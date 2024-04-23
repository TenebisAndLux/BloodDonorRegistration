CREATE TABLE Donors (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    MiddleName VARCHAR(50) NULL,
    DateOfBirth DATE NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Address VARCHAR(100) NULL,
    PhoneNumber VARCHAR(20) NULL,
    HospitalAffiliation VARCHAR(100) NULL,
    PassportData VARCHAR(20) NULL,
    InsuranceData VARCHAR(20) NULL,
    BloodType VARCHAR(5) NOT NULL,
    RhFactor VARCHAR(5) NOT NULL
);

CREATE TABLE MedicalHistory (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    DonorID INT NOT NULL,
    LastExaminationDate DATE NOT NULL,
    TestResults VARCHAR(255) NULL,
    DonationBan BIT NOT NULL,
    CONSTRAINT FK_DonorID_MedicalHistory FOREIGN KEY (DonorID) REFERENCES Donors(ID)
);

CREATE TABLE BloodCollections (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    CollectionDate DATE NOT NULL,
    DonorID INT NOT NULL,
    CollectionType VARCHAR(50) NOT NULL,
    CONSTRAINT FK_DonorID_BloodCollections FOREIGN KEY (DonorID) REFERENCES Donors(ID)
);

CREATE TABLE Reports (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ReportType VARCHAR(50) NOT NULL,
    CreationDate DATE NOT NULL,
    ReportContent TEXT NULL,
    ReportFile VARBINARY(MAX) NULL
);

ALTER TABLE MedicalHistory
ADD CONSTRAINT FK_DonorID_MedicalHistory FOREIGN KEY (DonorID) REFERENCES Donors(ID);

ALTER TABLE BloodCollections
ADD CONSTRAINT FK_DonorID_BloodCollections FOREIGN KEY (DonorID) REFERENCES Donors(ID);
