import pandas as pd
import os


def main():
    drugs_genes_path = "data/drugGenes_all.csv"
    genes_phenos_diseases_path = "data/genePhenoDis_all.csv"
    genes_proteins_seqs_path = "data/geneProSeq_all.csv"

    drugs_genes = {}
    genes_phenos_diseases = {}
    genes_proteins_seqs = {}

    if os.path.exists(drugs_genes_path):
        print("Loading", drugs_genes_path)
        drugs_genes = pd.read_csv(drugs_genes_path)
        drugs_genes.rename(columns={'gene':'geneSym'}, inplace=True)

    if os.path.exists(genes_phenos_diseases_path):
        print("Loading",genes_phenos_diseases_path)
        genes_phenos_diseases = pd.read_csv(genes_phenos_diseases_path)

    if os.path.exists(genes_proteins_seqs_path):
        print("Loading", genes_proteins_seqs_path)
        genes_proteins_seqs = pd.read_csv(genes_proteins_seqs_path)

    df = pd.merge(genes_phenos_diseases, genes_proteins_seqs, on='geneSym')
    print(df.info())
    # genes relation
    genes = df[['geneSym', 'geneName', 'proteinId', 'proteinName', 'geneLoc']]

    # phenotypes relation
    phenotypes = df[['geneSym', 'phenotype']]
    phenotypes['variations'] = 0

    # proteins relation
    # proteinId is some jibberish. would be nice to have the pdb id
    proteins = df[['proteinId', 'proteinName', 'diseases', 'proteinSeq']]

    # TODO: split lists into atoms so that data is in 1nf
    diseases = df[['diseases', 'phenotypeInheritance']]

    df = pd.merge(drugs_genes, genes_phenos_diseases, on='geneSym')

    treatments = df[['product_name', 'diseases', 'descr', 'route']]


    print(treatments.info())
    print(treatments.head())



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()