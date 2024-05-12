INSERT INTO Donors (FirstName, LastName, MiddleName, Address, PhoneNumber, PassportData, DateOfBirth, BloodType, RhFactor) VALUES 
    ('John', 'Doe', 'l', '123 Main St', '555-1234', 'ABC123456', '1990-05-15', 'A', '+'),
    ('Jane', 'Doe', 'x', '456 Oak St', '555-9876', 'CD123456', '1985-06-20', 'B', '-'),
    ('Jack', 'Smith', NULL, '789 Maple St', '555-5678', 'EF123456', '1975-07-10', 'AB', '+'),
    ('Jill', 'Smith', 'y', '321 Elm St', '555-1472', 'GH123456', '1995-12-05', 'A', '-'),
    ('James', 'Johnson', 'z', '951 Oak Ave', '555-9012', 'IJ123456', '1980-08-15', 'O', '+')

INSERT INTO MedicalHistory (DonorID, LastExaminationDate, TestResults, DonationBan) VALUES
    (1, '2021-10-20', 'Normal', FALSE),    (2, '2021-09-10', 'Normal', FALSE),
    (3, '2021-07-15', 'Elevated cholesterol', TRUE),    (4, '2021-10-10', 'Normal', FALSE),
    (5, '2021-09-05', 'Elevated blood pressure', TRUE);

INSERT INTO BloodCollections (CollectionDate, DonorID, CollectionType) VALUES
    ('2021-10-25', 1, 'Whole Blood'),    ('2021-10-15', 2, 'Plasma'),
    ('2021-08-20', 3, 'Platelets'),    ('2021-09-30', 4, 'Whole Blood'),
    ('2021-10-05', 5, 'Whole Blood');

INSERT INTO Reports (ReportType, CreationDate, ReportContent, ReportFile)
VALUES    ('Medical Report', '2021-10-30', 'Patient is in good health.', NULL),
    ('Blood Test Results', '2021-11-02', 'Cholesterol: 160 mg/dL', NULL),    ('Blood Test Results', '2021-10-05', 'Blood Pressure: 120/80 mmHg', NULL),
    ('Blood Test Results', '2021-09-15', 'Cholesterol: 240 mg/dL', NULL),    ('Blood Test Results', '2021-10-20', 'Blood Pressure: 140/90 mmHg', NULL);

INSERT INTO Doctors (FirstName, LastName, Position, Login, Password, email)
VALUES('John', 'Smith', 'Doctor', 'jsmith', '123', 'meazerg@gmail.com'),
('Jane', 'Doe', 'Nurse', 'jdoe', '123', 'meazerg@gmail.com'),('Jack', 'Brown', 'Surgeon', 'jbrown', '123', 'meazerg@gmail.com');
