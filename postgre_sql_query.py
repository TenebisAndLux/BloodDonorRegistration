import os
import psycopg2

HOST = os.environ.get('POSTGRES_HOST')
USER = os.environ.get('POSTGRES_USER')
PASSWD = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')
PORT = os.environ.get('POSTGRES_PORT')

schema_sql = """
-- Удаление таблиц
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

-- Создание таблиц
CREATE TABLE MedicalInstitution (
   InstitutionCode      SERIAL PRIMARY KEY,
   NameOfInstitution    VARCHAR(255) NOT NULL,
   Address              VARCHAR(255) NOT NULL,
   ContactPhoneNumber   VARCHAR(15)  NOT NULL,
   Email                VARCHAR(255) NOT NULL,
   TypeOfInstitution    VARCHAR(100) NOT NULL
);
CREATE TABLE Doctor (
   InstitutionCode      INT4 NOT NULL REFERENCES MedicalInstitution(InstitutionCode),
   ServiceNumber        INT4 NOT NULL,
   Name                 VARCHAR(100) NOT NULL,
   SecondName           VARCHAR(100) NOT NULL,
   JobTitle             VARCHAR(100) NOT NULL,
   Login                VARCHAR(50)  NOT NULL,
   Password             VARCHAR(255) NOT NULL,
   Email                VARCHAR(255) NOT NULL,
   PRIMARY KEY (InstitutionCode, ServiceNumber)
);
CREATE TABLE MedicalHistory (
   HistoryNumber        SERIAL PRIMARY KEY,
   PassportDetails      INT4 NOT NULL,
   DateOfLastExamination DATE NOT NULL,
   AnalysisResults      TEXT,
   BanOnDonation        BOOLEAN DEFAULT FALSE
);
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
CREATE TABLE BloodCollectionType (
   CollectionTypeCode   SERIAL PRIMARY KEY,
   Name                 VARCHAR(100) NOT NULL
);
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
CREATE TABLE DoctorDonor (
   PassportData         INT4 NOT NULL,
   InstitutionCode      INT4 NOT NULL,
   DonationRegistrationCode INT4 NOT NULL,
   ServiceNumber        INT4 NOT NULL,
   PRIMARY KEY (PassportData, InstitutionCode, DonationRegistrationCode, ServiceNumber),
   FOREIGN KEY (PassportData, InstitutionCode) REFERENCES Donor(PassportData, InstitutionCode),
   FOREIGN KEY (DonationRegistrationCode, ServiceNumber) REFERENCES Doctor(InstitutionCode, ServiceNumber)
);
CREATE TABLE DonorDoctor (
   DonationRegistrationCode INT4 NOT NULL,
   ServiceNumber        INT4 NOT NULL,
   PassportData         INT4 NOT NULL,
   InstitutionCode      INT4 NOT NULL,
   PRIMARY KEY (DonationRegistrationCode, ServiceNumber, PassportData, InstitutionCode),
   FOREIGN KEY (DonationRegistrationCode, ServiceNumber) REFERENCES Doctor(InstitutionCode, ServiceNumber),
   FOREIGN KEY (PassportData, InstitutionCode) REFERENCES Donor(PassportData, InstitutionCode)
);
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
CREATE TABLE DonorMedicalExaminationResults (
   Number               INT4 NOT NULL REFERENCES MedicalExamination(Number),
   PassportData         INT4 NOT NULL,
   InstitutionCode      INT4 NOT NULL,
   PRIMARY KEY (Number, PassportData, InstitutionCode),
   FOREIGN KEY (PassportData, InstitutionCode) REFERENCES Donor(PassportData, InstitutionCode)
);
"""

data_sql = """-- Вставка в MedicalInstitution
INSERT INTO MedicalInstitution (NameOfInstitution, Address, ContactPhoneNumber, Email, TypeOfInstitution) VALUES
('Центр крови №1', 'Москва, ул. Красная, д.1', '+74951234567', 'blood1@example.com', 'Городской центр крови'),
('Центр крови №2', 'Санкт-Петербург, Невский пр-т, д.10', '+78121234567', 'blood2@example.com', 'Областной центр крови');

-- Вставка в Doctor
INSERT INTO Doctor (InstitutionCode, ServiceNumber, Name, SecondName, JobTitle, Login, Password, Email) VALUES
(1, 101, 'Иван', 'Петров', 'Трансфузиолог', 'ipetrov', 'pass123', 'ipetrov@example.com'),
(1, 102, 'Мария', 'Сидорова', 'Гематолог', 'msidorova', 'pass123', 'msidorova@example.com'),
(2, 201, 'Алексей', 'Смирнов', 'Терапевт', 'asmirnov', 'pass123', 'asmirnov@example.com'),
(2, 202, 'Ольга', 'Иванова', 'Иммунолог', 'oivanova', 'pass123', 'oivanova@example.com');

-- Вставка в MedicalHistory
INSERT INTO MedicalHistory (PassportDetails, DateOfLastExamination, AnalysisResults, BanOnDonation) VALUES
(1001, '2024-05-01', 'Все в норме', false),
(1002, '2024-04-20', 'Высокий гемоглобин', false),
(1003, '2024-03-15', 'Признаки анемии', true),
(1004, '2024-01-10', 'Все в порядке', false),
(1005, '2024-02-05', 'Инфекция - запрет', true),
(1006, '2024-04-01', 'В норме', false),
(1007, '2024-04-15', 'В норме', false),
(1008, '2024-03-30', 'Годен', false),
(1009, '2024-02-14', 'Низкий уровень железа', true),
(1010, '2024-01-01', 'Без отклонений', false);

-- Вставка в Donor
INSERT INTO Donor (PassportData, InstitutionCode, HistoryNumber, Name, SecondName, SurName, Birthday, Gender, Address, PhoneNumber, Polis, BloodGroup, RhFactor) VALUES
(1001, 1, 1, 'Андрей', 'Иванов', 'Петрович', '1990-01-01', 'М', 'Москва, ул. Ленина, д.1', '+79161234501', '1234567890', 'A', '+'),
(1002, 1, 2, 'Елена', 'Кузнецова', 'Игоревна', '1992-05-10', 'Ж', 'Москва, ул. Мира, д.5', '+79161234502', '1234567891', 'B', '+'),
(1003, 1, 3, 'Дмитрий', 'Соколов', 'Алексеевич', '1988-03-12', 'М', 'Москва, ул. Правды, д.8', '+79161234503', '1234567892', 'O', '-'),
(1004, 1, 4, 'Оксана', 'Лебедева', 'Павловна', '1995-06-25', 'Ж', 'Москва, ул. Садовая, д.3', '+79161234504', '1234567893', 'AB', '+'),
(1005, 1, 5, 'Максим', 'Зайцев', 'Юрьевич', '1985-11-11', 'М', 'Москва, ул. Лесная, д.2', '+79161234505', '1234567894', 'A', '-'),
(1006, 2, 6, 'Светлана', 'Морозова', 'Викторовна', '1991-08-18', 'Ж', 'СПб, ул. Фонтанка, д.7', '+79161234506', '1234567895', 'B', '+'),
(1007, 2, 7, 'Игорь', 'Титов', 'Денисович', '1993-12-30', 'М', 'СПб, ул. Рубинштейна, д.4', '+79161234507', '1234567896', 'O', '+'),
(1008, 2, 8, 'Анна', 'Крылова', 'Николаевна', '1996-04-04', 'Ж', 'СПб, ул. Литейный, д.6', '+79161234508', '1234567897', 'AB', '-'),
(1009, 2, 9, 'Руслан', 'Фролов', 'Олегович', '1987-09-09', 'М', 'СПб, ул. Маяковского, д.9', '+79161234509', '1234567898', 'A', '+'),
(1010, 2, 10, 'Наталья', 'Орлова', 'Георгиевна', '1994-07-07', 'Ж', 'СПб, ул. Московская, д.11', '+79161234510', '1234567899', 'B', '-');

-- Вставка в BloodCollectionType
INSERT INTO BloodCollectionType (Name) VALUES
('Цельная кровь'), ('Плазма'), ('Тромбоциты');

-- Вставка в BloodSupply
INSERT INTO BloodSupply (CollectionTypeCode, InstitutionCode, NumberStock, NumberCollections, BloodGroup, RhFactor, BloodVolume, ProcurementDate, BestBeforeDate, MedicalInstitutionCode) VALUES
(1, 1, 1, 5, 'A', '+', 450, '2025-04-01', '2025-07-01', 1),
(2, 1, 2, 3, 'B', '+', 600, '2025-04-15', '2025-07-15', 1),
(1, 2, 3, 2, 'O', '-', 400, '2025-03-20', '2025-06-20', 2);

-- Вставка в BloodCollection
INSERT INTO BloodCollection (BloodSupplyCollectionTypeCode, BloodBankInstitutionCode, NumberStock, Number, DonationRegistrationCode, ServiceNumber, PassportData, InstitutionCode, CollectionDate, PassportDetails, CollectionTypeCode) VALUES
(1, 1, 1, 1, 1, 101, 1001, 1, '2025-04-01', 1001, 1),
(2, 1, 2, 1, 1, 102, 1002, 1, '2025-04-15', 1002, 2),
(1, 2, 3, 1, 2, 201, 1006, 2, '2025-03-20', 1006, 1);

-- Вставка в DoctorDonor
INSERT INTO DoctorDonor (PassportData, InstitutionCode, DonationRegistrationCode, ServiceNumber) VALUES
(1001, 1, 1, 101),
(1002, 1, 1, 102),
(1006, 2, 2, 201);

-- Вставка в DonorDoctor
INSERT INTO DonorDoctor (DonationRegistrationCode, ServiceNumber, PassportData, InstitutionCode) VALUES
(1, 101, 1001, 1),
(1, 102, 1002, 1),
(2, 201, 1006, 2);

-- Вставка в MedicalExamination
INSERT INTO MedicalExamination (PassportData, InstitutionCode, DonationRegistrationCode, ServiceNumber, PassportDetails, DateOfExamination, SurveyResults, PersonnelNumber) VALUES
(1001, 1, 1, 101, 1001, '2025-04-01', 'Годен к сдаче крови', 555),
(1002, 1, 1, 102, 1002, '2025-04-15', 'Годна, уровень железа высокий', 556),
(1006, 2, 2, 201, 1006, '2025-03-20', 'Все показатели в норме', 557);

-- Вставка в DonorMedicalExaminationResults
INSERT INTO DonorMedicalExaminationResults (Number, PassportData, InstitutionCode) VALUES
(1, 1001, 1),
(2, 1002, 1),
(3, 1006, 2);
"""

try:
    connection = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWD,
        port=PORT,
        database=DB_NAME
    )
    connection.autocommit = True
    cursor = connection.cursor()

    print("Connected to database")

    # Удаление и создание таблиц
    cursor.execute(schema_sql)
    print("Database schema recreated successfully")

    # Вставка данных
    cursor.execute(data_sql)
    print("Data inserted successfully")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
