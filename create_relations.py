import pandas as pd
import os
import mysql.connector


def main():
    drugs_genes_path = "data/drugGenes_all.csv"
    genes_phenos_diseases_path = "data/genePhenoDis_all.csv"
    genes_proteins_seqs_path = "data/geneProSeq_all.csv"

    if not all([os.path.isfile(drugs_genes_path), genes_phenos_diseases_path, genes_proteins_seqs_path]):
        print("Missing some files in data dir")
        exit(1)

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

    # genes relation
    genes = df[['geneSym', 'geneName', 'proteinId', 'proteinName', 'geneLoc']]
    genes = genes.drop_duplicates()


    # phenotypes relation
    phenotypes = df[['geneSym', 'phenotype']].copy()
    phenotypes.loc['variations'] = 0
    phenotypes = phenotypes.drop_duplicates()

    # TODO: split disease lists into atoms so that data is in 1nf
    diseases = df[['diseases','phenotypeInheritance']]
    diseases = diseases.drop_duplicates()
    diseases.fillna('None')

    # proteins relation
    # proteinId is some jibberish. would be nice to have the pdb id
    proteins = df[['proteinId', 'proteinName', 'diseases', 'proteinSeq']]
    proteins = proteins.drop_duplicates('proteinId')

    df = pd.merge(drugs_genes, genes_phenos_diseases, on='geneSym')

    treatments = df[['product_name', 'diseases', 'descr', 'route']]
    treatments.drop_duplicates()

    print("Inserting items into database")

    # this order should match the one in sql/data.sql
    relations = [('disease',diseases), ('protein',proteins), ('gene',genes), ('phenotype',phenotypes), ('treatment',treatments)]
    for n,r in relations:
        print("saving",n)
        r.to_csv('csv/' + n + '.csv', index=False, na_rep='None', sep='~')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()