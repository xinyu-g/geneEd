# GeneEd
 This application provides a platform for users to learn about the genetics of diseases, as well as genetics of common appearance traits. Users can search for genes that are associated with disease names and phenotype descriptions as well as DNA or protein sequences. It makes the world of genetics easy to explore for younger students or curious adults and would be of great use to high school science classrooms.

## Installation and Usage
0. Clone the repository to your computer
   ```
   git clone https://github.com/xinyu-g/geneEd.git
   ```

1. Create a new conda environment for GeneEd. If you do not have conda, install Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html) first.
    ```
    conda env create -f environment.yaml
    ```
## Building the database.

1. concatenate all drugsGenes, genePhenoDis, and geneProSeq into 3 files. Remove duplicate headers (column metadata). Place these files in data/.
2. Run `create_relations.py` to get 5 csv files representing the relations.
3. Copy the generated SQL files to MySQL's uploads directory. On windows, this is in `C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\`. This is the only directoru that MySQL trusts by default.
4. Run `sql/data.sql` in MySQL workbench or a shell to build the schema and insert data into all tables but the gene table.
5. use `sql/users.sql` to create the user and favoriyes table.
6. Run `csv2sql.py` on gene.csv to generate gene.sql. This will take some time but reports progress.
7. Log in to the database with a commandline client. Select the geneEd database. Run `source gene.sql` to populate the database. Some records will fail to insert but this is okay. `SELECT COUNT(*) FROM gene` should return 1024.
8. The database should be complete.

Alternatively, use the dumpfile Hunter created to generate the entire database. (I generated this late last night and did not test).

## Running the flask app
0. Make sure that you have installed flask with conda, and have the MySQL server running with the database populated and accessible on localhost.

1. Set the `FLASK_APP` environment variable (windows)
   ```
   > set FLASK_APP=geneEd
   ```

2. Set the `FLASK_ENV` environmen variable (windows)
   ```
   > set FLASK_ENV=development
   ```
3. Start the server with the following command:
   ```
   flask run
   ```
4. Flask starts on 127.0.0.1:5000 by default. Currently, genes can be searched for by symbol. To search for a symbol, navigate to [127.0.0.1:5000/search/genesymbol](127.0.0.1:5000/search/genesymbol). Try searching for TP53 or ACOX1. The symbol, name, and locaiton currently get displayed. Invalid queries will show an error page. 
