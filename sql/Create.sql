CREATE TABLE Donors ( 
    ID SERIAL PRIMARY KEY, 
    FirstName VARCHAR(50) NOT NULL, 
    LastName VARCHAR(50) NOT NULL, 
    MiddleName VARCHAR(50), 
    DateOfBirth DATE NOT NULL, 
    Gender VARCHAR(10) NOT NULL, 
    Address VARCHAR(100), 
    PhoneNumber VARCHAR(20), 
    HospitalAffiliation VARCHAR(100), 
    PassportData VARCHAR(20), 
    InsuranceData VARCHAR(20), 
    BloodType VARCHAR(5) NOT NULL, 
    RhFactor VARCHAR(5) NOT NULL 
);

CREATE TABLE MedicalHistory (
    ID SERIAL PRIMARY KEY,
    DonorID INT NOT NULL,
    LastExaminationDate DATE NOT NULL,
    TestResults VARCHAR(255),
    DonationBan BOOLEAN NOT NULL,
    CONSTRAINT FK_DonorID_MedicalHistory FOREIGN KEY (DonorID) REFERENCES Donors(ID)
);

CREATE TABLE BloodCollections (
    ID SERIAL PRIMARY KEY,
    CollectionDate DATE NOT NULL,
    DonorID INT NOT NULL,
    CollectionType VARCHAR(50) NOT NULL,
    CONSTRAINT FK_DonorID_BloodCollections FOREIGN KEY (DonorID) REFERENCES Donors(ID)
);

CREATE TABLE Reports (
    ID SERIAL PRIMARY KEY,
    ReportType VARCHAR(50) NOT NULL,
    CreationDate DATE NOT NULL,
    ReportContent TEXT,
    ReportFile BYTEA
);

CREATE TABLE Doctors (
    ID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Position VARCHAR(50) NOT NULL,
    Login VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(50) NOT NULL,
    email VARCHAR(50)
);