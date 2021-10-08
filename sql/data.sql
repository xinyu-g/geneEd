CREATE TABLE gene(
    symbol VARCHAR(8) PRIMARY,
    fullName VARCHAR(255),
    proteinId VARCHAR(255),
    proteinName VARCHAR(511),
    locus VARCHAR(255),
    popularity INT DEFAULT 0,
    FOREIGN KEY (fullName) REFERENCES protein
)

CREATE TABLE phenotype(
    symbol VARCHAR(8) PRIMARY KEY,
    traits VARCHAR(500) NOT NULL,
    variations INT DEFAULT 0,
    FOREIGN KEY (symbol) REFERENCES gene,
)

CREATE TABLE protein(
    proteinName VARCHAR(255) PRIMARY KEY,
    diseaseName VARCHAR(255),
    seq TEXT.
    FOREIGN KEY (diseaseName) REFERENCES disease
)

CREATE TABLE disease(
    diseaseName VARCHAR(255) PRIMARY KEY,
    mutationType VARCHAR(30)
)

CREATE TABLE treatment(
    treatmentName VARCHAR(255) PRIMARY KEY,
    diseaseName VARCHAR(255),
    treatmentDescription VARCHAR(100),
    treatmentLocation VARCHAR(255),
    FOREIGN KEY (diseaseName) REFERENCES disease
)