DROP DATABASE IF EXISTS geneEd;
CREATE DATABASE geneEd;
use geneEd;

CREATE TABLE disease(
    diseaseName VARCHAR(255),
    mutationType VARCHAR(64),
    PRIMARY KEY (diseaseName, mutationType)
);

CREATE TABLE protein(
	proteinId VARCHAR(32) PRIMARY KEY,
    proteinName VARCHAR(1024),
    diseaseName VARCHAR(512),
    sequence TEXT,
    FOREIGN KEY (diseaseName) REFERENCES disease(diseaseName)
);

CREATE TABLE gene(
    symbol VARCHAR(8) PRIMARY KEY,
    fullName VARCHAR(255),
    proteinId VARCHAR(32),
    proteinName VARCHAR(1024),
    locus VARCHAR(255),
    sequence LONGTEXT,
    popularity INT DEFAULT 0,
    FOREIGN KEY (proteinId) REFERENCES protein(proteinId)
);

CREATE TABLE phenotype(
    symbol VARCHAR(8) PRIMARY KEY,
    traits VARCHAR(500) NOT NULL,
    variations INT DEFAULT 0,
    FOREIGN KEY (symbol) REFERENCES gene(symbol)
);

CREATE TABLE treatment(
    treatmentName VARCHAR(512),
    diseaseName VARCHAR(512),
    treatmentDescription VARCHAR(2000),
    treatmentLocation VARCHAR(255),
    FOREIGN KEY (diseaseName) REFERENCES disease(diseaseName)
);

------------------------------------

SET FOREIGN_KEY_CHECKS=0;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/disease.csv' 
INTO TABLE disease 
FIELDS TERMINATED BY '~' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/protein.csv' 
INTO TABLE protein 
FIELDS TERMINATED BY '~' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- LOAD DATA LOW_PRIORITY INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/gene.csv' 
-- INTO TABLE gene 
-- FIELDS TERMINATED BY '~' 
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/phenotype.csv' 
INTO TABLE phenotype 
FIELDS TERMINATED BY '~'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/treatment.csv' 
INTO TABLE treatment 
FIELDS TERMINATED BY '~' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;