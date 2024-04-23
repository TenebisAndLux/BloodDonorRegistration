CREATE TABLE Donors (
    ID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    MiddleName VARCHAR(50),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    Address VARCHAR(100),
    PhoneNumber VARCHAR(20),
    HospitalAffiliation VARCHAR(100),
    PassportData VARCHAR(20),
    InsuranceData VARCHAR(20),
    BloodType VARCHAR(5),
    RhFactor VARCHAR(5)
);

CREATE TABLE MedicalHistory (
    ID INT PRIMARY KEY,
    DonorID INT,
    LastExaminationDate DATE,
    TestResults VARCHAR(255),
    DonationBan BIT,
    CONSTRAINT FK_DonorID_MedicalHistory FOREIGN KEY (DonorID) REFERENCES Donors(ID)
);

CREATE TABLE BloodCollections (
    ID INT PRIMARY KEY,
    CollectionDate DATE,
    DonorID INT,
    CollectionType VARCHAR(50),
    CONSTRAINT FK_DonorID_BloodCollections FOREIGN KEY (DonorID) REFERENCES Donors(ID)
);

CREATE TABLE Reports (
    ID INT PRIMARY KEY,
    ReportType VARCHAR(50),
    CreationDate DATE,
    ReportContent TEXT,
    ReportFile VARBINARY(MAX)
);

ALTER TABLE MedicalHistory
ADD CONSTRAINT FK_DonorID_MedicalHistory FOREIGN KEY (DonorID) REFERENCES Donors(ID);

ALTER TABLE BloodCollections
ADD CONSTRAINT FK_DonorID_BloodCollections FOREIGN KEY (DonorID) REFERENCES Donors(ID);

ALTER TABLE Reports
ADD CONSTRAINT FK_MedicalHistoryID_Reports FOREIGN KEY (MedicalHistoryID) REFERENCES MedicalHistory(ID);