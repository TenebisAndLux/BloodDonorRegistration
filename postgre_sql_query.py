from config import host, user, password, port, db_name
import psycopg2

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=db_name
    )
    connection.autocommit = True
    cursor = connection.cursor()
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record)
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE Donors ( 
            ID SERIAL PRIMARY KEY, 
            FirstName VARCHAR(50) NOT NULL, 
            LastName VARCHAR(50) NOT NULL, 
            MiddleName VARCHAR(50), 
            DateOfBirth DATE NOT NULL, 
            Gender VARCHAR(10) NOT NULL, 
            Address VARCHAR(100), 
            PhoneNumber VARCHAR(20), 
            HospitalAffiliation VARCHAR(100), 
            PassportData VARCHAR(50), 
            InsuranceData VARCHAR(50), 
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
        );""")

        print('Table created successfully in PostgreSQL')

        cursor.execute("""
        INSERT INTO Donors (FirstName, LastName, MiddleName, DateOfBirth, Gender, Address, PhoneNumber, HospitalAffiliation, PassportData, InsuranceData, BloodType, RhFactor)
        VALUES
            ('John', 'Doe', 'l', '1990-05-15', 'M', '123 Main St', '555-1234', 'St. Mary Hospital', 'ABC123456', 'Some', 'A', '+'),
            ('Jane', 'Doe', 'x', '1985-06-20', 'F', '456 Oak St', '555-9876', 'St. John Hospital', 'CD123456', 'Another', 'B', '-'),
            ('Jack', 'Smith', NULL, '1975-07-10', 'M', '789 Maple St', '555-5678', 'St. Mary Hospital', 'EF123456', 'Some I', 'AB', '+'),
            ('Jill', 'Smith', 'y', '1995-12-05', 'F', '321 Elm St', '555-1472', 'St. John Hospital', 'GH123456', 'Another In', 'A', '-'),
            ('James', 'Johnson', 'z', '1980-08-15', 'M', '951 Oak Ave', '555-9012', 'St. Mary Hospital', 'IJ123456', 'Some Ins', 'O', '+');
        
        INSERT INTO Reports (ReportType, CreationDate, ReportContent, ReportFile)
        VALUES
            ('Medical Report', '2020-01-05', 'Patient is in good health.', NULL),
            ('Blood Test Results', '2020-01-10', 'Cholesterol: 160 mg/dL', NULL),
            ('Blood Test Results', '2020-02-05', 'Blood Pressure: 120/80 mmHg', NULL),
            ('Blood Test Results', '2020-03-15', 'Cholesterol: 240 mg/dL', NULL),
            ('Blood Test Results', '2020-04-05', 'Blood Pressure: 140/90 mmHg', NULL),
            ('Blood Test Results', '2020-05-10', 'Cholesterol: 180 mg/dL', NULL),
            ('Blood Test Results', '2020-06-15', 'Blood Pressure: 160/100 mmHg', NULL),
            ('Blood Test Results', '2020-07-05', 'Cholesterol: 100 mg/dL', NULL),
            ('Blood Test Results', '2020-08-15', 'Blood Pressure: 130/85 mmHg', NULL),
            ('Blood Test Results', '2020-09-05', 'Cholesterol: 120 mg/dL', NULL),
            ('Blood Test Results', '2020-10-15', 'Blood Pressure: 145/95 mmHg', NULL),
            ('Medical Report', '2020-11-05', 'Patient has a cold.', NULL),
            ('Blood Test Results', '2020-11-10', 'Cholesterol: 100 mg/dL', NULL),
            ('Blood Test Results', '2020-12-05', 'Blood Pressure: 120/80 mmHg', NULL);
                       
        INSERT INTO BloodCollections (CollectionDate, DonorID, CollectionType)
        VALUES
            ('2020-01-05', 1, 'Whole Blood'),
            ('2020-02-15', 1, 'Plasma'),
            ('2020-03-05', 2, 'Platelets'),
            ('2020-04-10', 2, 'Whole Blood'),
            ('2020-05-15', 3, 'Plasma'),
            ('2020-06-05', 3, 'Platelets'),
            ('2020-07-10', 3, 'Whole Blood'),
            ('2020-08-05', 4, 'Plasma'),
            ('2020-09-15', 4, 'Platelets'),
            ('2020-10-05', 4, 'Whole Blood'),
            ('2020-11-05', 5, 'Whole Blood'),
            ('2020-12-15', 5, 'Plasma');
        
        INSERT INTO Doctors (FirstName, LastName, Position, Login, Password, email)
        VALUES
            ('John', 'Doe', 'Doctor', 'johndoe', '123', 'johndoe@gmail.com'),
            ('Jane', 'Smith', 'Nurse', 'janesmith', '123', 'janesmith@gmail.com'),
            ('Jack', 'Johnson', 'Surgeon', 'jackjohnson', '123', 'jackjohnson@gmail.com'),
            ('Jill', 'Williams', 'Doctor', 'jillwilliams', '123', 'jillwilliams@gmail.com'),
            ('James', 'Brown', 'Nurse', 'jamesbrown', '123', 'jamesbrown@gmail.com');
        
        INSERT INTO MedicalHistory (DonorID, LastExaminationDate, TestResults, DonationBan) VALUES
            (1, '2021-10-20', 'Normal', FALSE),    (2, '2021-09-10', 'Normal', FALSE),
            (3, '2021-07-15', 'Elevated cholesterol', TRUE),    (4, '2021-10-10', 'Normal', FALSE),
            (5, '2021-09-05', 'Elevated blood pressure', TRUE);
        
        INSERT INTO BloodCollections (CollectionDate, DonorID, CollectionType) VALUES
            ('2021-10-25', 1, 'Whole Blood'),    ('2021-10-15', 2, 'Plasma'),
            ('2021-08-20', 3, 'Platelets'),    ('2021-09-30', 4, 'Whole Blood'),
            ('2021-10-05', 5, 'Whole Blood');
        """)
        print('Table insert successfully in PostgreSQL')

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
