-- Удаление таблиц в правильном порядке
DROP TABLE IF EXISTS DonorMedicalExaminationResults;
DROP TABLE IF EXISTS MedicalExamination;
DROP TABLE IF EXISTS DoctorDonor;
DROP TABLE IF EXISTS DonorDoctor;
DROP TABLE IF EXISTS BloodCollection;
DROP TABLE IF EXISTS BloodSupply;
DROP TABLE IF EXISTS BloodCollectionType;
DROP TABLE IF EXISTS Donor;
DROP TABLE IF EXISTS Doctor;
DROP TABLE IF EXISTS MedicalHistory;
DROP TABLE IF EXISTS MedicalInstitution;

-- Создание таблицы MedicalInstitution
CREATE TABLE MedicalInstitution (
   InstitutionCode      SERIAL PRIMARY KEY,
   NameOfInstitution    VARCHAR(255) NOT NULL,
   Address              VARCHAR(255) NOT NULL,
   ContactPhoneNumber   VARCHAR(15)  NOT NULL,
   Email                VARCHAR(255) NOT NULL,
   TypeOfInstitution    VARCHAR(100) NOT NULL
);

-- Создание таблицы Doctor
CREATE TABLE Doctor (
   InstitutionCode      INT4 NOT NULL REFERENCES MedicalInstitution(InstitutionCode),
   ServiceNumber        INT4 NOT NULL,
   Role                 VARCHAR(100) NOT NULL,
   Name                 VARCHAR(100) NOT NULL,
   SecondName           VARCHAR(100) NOT NULL,
   JobTitle             VARCHAR(100) NOT NULL,
   Login                VARCHAR(50)  NOT NULL,
   Password             VARCHAR(255) NOT NULL,
   Email                VARCHAR(255) NOT NULL,
   PRIMARY KEY (InstitutionCode, ServiceNumber)
);

-- Создание таблицы MedicalHistory
CREATE TABLE MedicalHistory (
   HistoryNumber        SERIAL PRIMARY KEY,
   PassportDetails      INT4 NOT NULL,
   DateOfLastExamination DATE NOT NULL,
   AnalysisResults      TEXT,
   BanOnDonation        BOOLEAN DEFAULT FALSE
);

-- Создание таблицы Donor
CREATE TABLE Donor (
   PassportData         INT4 NOT NULL,
   InstitutionCode      INT4 NOT NULL REFERENCES MedicalInstitution(InstitutionCode),
   HistoryNumber        INT4 REFERENCES MedicalHistory(HistoryNumber),
   Name                 VARCHAR(100) NOT NULL,
   SecondName           VARCHAR(100) NOT NULL,
   SurName              VARCHAR(100) NOT NULL,
   Birthday             DATE NOT NULL,
   Gender               VARCHAR(10)  NOT NULL,
   Address              VARCHAR(255) NOT NULL,
   PhoneNumber          VARCHAR(15)  NOT NULL,
   Polis                VARCHAR(20)  NOT NULL,
   BloodGroup           VARCHAR(3)   NOT NULL,
   RhFactor             VARCHAR(1)   NOT NULL,
   PRIMARY KEY (PassportData, InstitutionCode)
);

-- Создание таблицы BloodCollectionType
CREATE TABLE BloodCollectionType (
   CollectionTypeCode   SERIAL PRIMARY KEY,
   Name                 VARCHAR(100) NOT NULL
);

-- Создание таблицы BloodSupply
CREATE TABLE BloodSupply (
   CollectionTypeCode   INT4 NOT NULL REFERENCES BloodCollectionType(CollectionTypeCode),
   InstitutionCode      INT4 NOT NULL REFERENCES MedicalInstitution(InstitutionCode),
   NumberStock          INT4 NOT NULL,
   NumberCollections    INT4,
   BloodGroup           VARCHAR(3),
   RhFactor             VARCHAR(1),
   BloodVolume          FLOAT8,
   ProcurementDate      DATE,
   BestBeforeDate       DATE,
   MedicalInstitutionCode INT4 REFERENCES MedicalInstitution(InstitutionCode),
   PRIMARY KEY (CollectionTypeCode, InstitutionCode, NumberStock)
);

-- Создание таблицы BloodCollection
CREATE TABLE BloodCollection (
   BloodSupplyCollectionTypeCode INT4 NOT NULL,
   BloodBankInstitutionCode INT4 NOT NULL,
   NumberStock          INT4 NOT NULL,
   Number               INT4 NOT NULL,
   DonationRegistrationCode INT4,
   ServiceNumber        INT4,
   PassportData         INT4,
   InstitutionCode      INT4,
   CollectionDate       DATE,
   PassportDetails      INT4,
   CollectionTypeCode   INT4 REFERENCES BloodCollectionType(CollectionTypeCode),
   PRIMARY KEY (BloodSupplyCollectionTypeCode, BloodBankInstitutionCode, NumberStock, Number),
   FOREIGN KEY (DonationRegistrationCode, ServiceNumber) REFERENCES Doctor(InstitutionCode, ServiceNumber),
   FOREIGN KEY (PassportData, InstitutionCode) REFERENCES Donor(PassportData, InstitutionCode),
   FOREIGN KEY (BloodSupplyCollectionTypeCode, BloodBankInstitutionCode, NumberStock)
      REFERENCES BloodSupply(CollectionTypeCode, InstitutionCode, NumberStock)
);

-- Создание таблицы DoctorDonor
CREATE TABLE DoctorDonor (
   PassportData         INT4 NOT NULL,
   InstitutionCode      INT4 NOT NULL,
   DonationRegistrationCode INT4 NOT NULL,
   ServiceNumber        INT4 NOT NULL,
   PRIMARY KEY (PassportData, InstitutionCode, DonationRegistrationCode, ServiceNumber),
   FOREIGN KEY (PassportData, InstitutionCode) REFERENCES Donor(PassportData, InstitutionCode),
   FOREIGN KEY (DonationRegistrationCode, ServiceNumber) REFERENCES Doctor(InstitutionCode, ServiceNumber)
);

-- Создание таблицы DonorDoctor
CREATE TABLE DonorDoctor (
   DonationRegistrationCode INT4 NOT NULL,
   ServiceNumber        INT4 NOT NULL,
   PassportData         INT4 NOT NULL,
   InstitutionCode      INT4 NOT NULL,
   PRIMARY KEY (DonationRegistrationCode, ServiceNumber, PassportData, InstitutionCode),
   FOREIGN KEY (DonationRegistrationCode, ServiceNumber) REFERENCES Doctor(InstitutionCode, ServiceNumber),
   FOREIGN KEY (PassportData, InstitutionCode) REFERENCES Donor(PassportData, InstitutionCode)
);

-- Создание таблицы MedicalExamination
CREATE TABLE MedicalExamination (
   Number               SERIAL PRIMARY KEY,
   PassportData         INT4,
   InstitutionCode      INT4,
   DonationRegistrationCode INT4,
   ServiceNumber        INT4,
   PassportDetails      INT4,
   DateOfExamination    DATE,
   SurveyResults        TEXT,
   PersonnelNumber      INT4,
   FOREIGN KEY (DonationRegistrationCode, ServiceNumber) REFERENCES Doctor(InstitutionCode, ServiceNumber),
   FOREIGN KEY (PassportData, InstitutionCode) REFERENCES Donor(PassportData, InstitutionCode)
);

-- Создание таблицы DonorMedicalExaminationResults
CREATE TABLE DonorMedicalExaminationResults (
   Number               INT4 NOT NULL REFERENCES MedicalExamination(Number),
   PassportData         INT4 NOT NULL,
   InstitutionCode      INT4 NOT NULL,
   PRIMARY KEY (Number, PassportData, InstitutionCode),
   FOREIGN KEY (PassportData, InstitutionCode) REFERENCES Donor(PassportData, InstitutionCode)
);