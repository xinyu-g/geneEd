import pandas as pd
import ncbi
import omim
import postgre
import consts as c
import entrezpy.conduit
from loguru import logger
import sys
import datetime
import random
import os.path
import os
from pathlib import Path


def findSeq(geneList, con, df):

    logger.info('Retrieving sequence data ...')
    genes = list()
    for geneSym in geneList:
        logger.debug("findSeq geneSym: {}", geneSym)
        query = {'db':'gene', 'term': geneSym + '[sym] AND human[ORGN]'} 
        
        gene = {'geneSym': geneSym}
        fetchGene = con.new_pipeline()
        sid = fetchGene.add_search(query)
        lid = fetchGene.add_link({'cmd':'neighbor_history', 'db':'Nucleotide'}, dependency=sid)
        lid = fetchGene.add_search({'cmd':'neighbor_history'}, dependency=lid)
        fid = fetchGene.add_fetch({'retmax': 1, 'retmode':'xml','rettype':'fasta'}, dependency=lid, analyzer=ncbi.SeqAnalyzer())
        
        fetchG = con.new_pipeline()
        sid1 = fetchG.add_search(query)
        fid1 = fetchG.add_fetch({'retmax': 1, 'retmode':'xml','rettype':'fasta'}, dependency=sid1, analyzer=ncbi.GeneAnalyzer())
        

        fetchProtein = con.new_pipeline()
        sid2 = fetchProtein.add_search(query)
        lid2 = fetchProtein.add_link({'cmd':'neighbor_history', 'db':'protein'}, dependency=sid2)
        lid2 = fetchProtein.add_search({'cmd':'neighbor_history'}, dependency=lid2)
        fid2 = fetchProtein.add_fetch({'retmax': 1, 'retmode':'xml','rettype':'fasta'}, dependency=lid2, analyzer=ncbi.proteinAnalyzer())
        protein_res = con.run(fetchProtein).get_result()
        
        
        g_res = con.run(fetchG).get_result()

        for i in g_res.gene_records:
            gene.update({
                'geneLoc': g_res.gene_records[i].loc
            })
        
        res = con.run(fetchGene).get_result()

        
        for i in res.seq_records:
            gene.update({
                'geneSeq': res.seq_records[i].sequence
            })
            

        for i in protein_res.protein_records:
            gene.update({
                'proteinId': protein_res.protein_records[i].pid,
                'proteinName': protein_res.protein_records[i].pname,
                'proteinSeq': protein_res.protein_records[i].pSquence
                })
        genes.append(gene)
    # logger.debug("genes: {}", genes)
    gene_ = pd.DataFrame.from_records(genes, index=['geneSym'])
    df = pd.concat([df, gene_])
    return df 


def findPhenotype(geneList, df):
    logger.info('retrieving phenotype, diseases data ...')
    genes = list()
    for geneSym in geneList:
        logger.debug("find Pheno Disease GeneSym: {}", geneSym)
        gene = omim.getGene(geneSym)
        if not gene: return df
        genes.append(gene)
    # logger.debug("genes: {}", genes)
    gene_ = pd.DataFrame.from_records(genes, index=['geneSym'])
    df = pd.concat([df, gene_])

    return df

def findDrugs(geneList, df):
    logger.info("retrieving drugs data....")
    for geneSym in geneList:
        logger.debug("find drugs geneSym: {}", geneSym)
        drug_ = postgre.get_data(geneSym)
        df = pd.concat([df, drug_])
    
    return df

def getGeneSymbols(df, column, alpha, n, exist=list()):
    tmp = df[df[column].str.startswith(alpha, na=False)]
    lst = tmp[~tmp[column].isin(exist)][column].tolist()
    if len(lst) == 0: return
    if len(lst) <= n:
        return lst
    return random.sample(lst, n)

    
    

def main():
    con = entrezpy.conduit.Conduit(c.EMAIL, c.API, threads=5)
    genes = pd.read_json('genes.json', orient='records')
    filepath = './data/'
    paths = {
                'geneProteinSeq': os.path.join(filepath, 'geneProSeq'),
                'genePhenoDis': os.path.join(filepath, 'genePhenoDis'),
                'drugGenes': os.path.join(filepath, 'drugGenes')
            }
    for k,v in paths.items():
        logger.debug("path: {}", v)
        Path(v).mkdir(parents=True, exist_ok=True)
    for alpha in c.ALPHABETS:
        logger.info(f'retrieving data for genes category {alpha}')
        
        # geneProteinSeq = pd.DataFrame()
        # genePhenoDis = pd.DataFrame()
        # geneDrugs = pd.DataFrame()
        geneProteinSeq = pd.read_csv(f'{paths["geneProteinSeq"]}/gene_protein_sequence_{alpha}.csv', index_col='geneSym')
        genePhenoDis = pd.read_csv(f'{paths["genePhenoDis"]}/gene_phenotype_diseases_{alpha}.csv', index_col='geneSym')
        geneDrugs = pd.read_csv(f'{paths["drugGenes"]}/drugs_gene_{alpha}.csv', index_col='product_name')
        # logger.debug("type: {}", type(genePhenoDis.index.tolist()))
        genes_list = getGeneSymbols(genes, 'symbol', alpha, 50, genePhenoDis.index.tolist())
        logger.debug("genes: {}, type: {}", genes_list, type(genes_list))

        if not genes_list: continue

        geneProteinSeq = findSeq(genes_list, con, geneProteinSeq)
        genePhenoDis = findPhenotype(genes_list, genePhenoDis)
        geneDrugs = findDrugs(genes_list, geneDrugs)

        if not geneProteinSeq.empty:
            geneProteinSeq.to_csv(f'{paths["geneProteinSeq"]}/gene_protein_sequence_{alpha}.csv')
        if not genePhenoDis.empty:
            genePhenoDis.to_csv(f'{paths["genePhenoDis"]}/gene_phenotype_diseases_{alpha}.csv')
        if not geneDrugs.empty:
            geneDrugs.to_csv(f'{paths["drugGenes"]}/drugs_gene_{alpha}.csv')



def init_logger():
    """Initialize logger."""
    console = True
    level = "DEBUG"
    path = "./logs"
    today = datetime.datetime.today()
    date = today.strftime("%Y%m%d")
    retention = "10 days"
    rotation = "20 MB"

    logger.remove()
    if console:
        logger.add(sys.stdout, colorize=True, level=level)

    logger.add(
        f"{path}/{date}.log",
        level=level,
        retention=retention,
        rotation=rotation,
        colorize=True,
        enqueue=True,
    )
    logger.info("logger init successfully.")

if __name__ == "__main__":
    main()