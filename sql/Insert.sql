INSERT INTO Donors (ID, FirstName, LastName, MiddleName, DateOfBirth, Gender, Address, PhoneNumber, HospitalAffiliation, PassportData, InsuranceData, BloodType, RhFactor) 
VALUES
	(1, 'John', 'Doe', 'l', '1990-05-15', 'Male', '123 Main St', '555-1234', 'City Hospital', 'AB123456', 'XYZ789', 'A', '+'),
	(2, 'Jane', 'Doe', 'x', '1985-06-20', 'Female', '456 Oak St', '555-9876', 'County Hospital', 'CD234567', 'XYZ012', 'B', '-'),
	(3, 'Jack', 'Smith', '', '1975-07-10', 'Male', '789 Maple St', '555-5678', 'State Hospital', 'EF345678', 'XYZ890', 'AB', '+'),
	(4, 'Jill', 'Smith', 'y', '1995-12-05', 'Female', '321 Elm St', '555-1472', 'City Clinic', 'GH456789', 'XYZ901', 'A', '-'),
	(5, 'James', 'Johnson', 'z', '1980-08-15', 'Male', '951 Oak Ave', '555-9012', 'Community Clinic', 'IJ567890', 'XYZ098', 'O', '+');

INSERT INTO MedicalHistory (ID, DonorID, LastExaminationDate, TestResults, DonationBan) 
VALUES
	(1, 1, '2021-10-20', 'Normal', 0),
	(2, 2, '2021-09-10', 'Normal', 0),
	(3, 3, '2021-07-15', 'Elevated cholesterol', 1),
	(4, 4, '2021-10-10', 'Normal', 0),
	(5, 5, '2021-09-05', 'Elevated blood pressure', 1);

INSERT INTO BloodCollections (ID, CollectionDate, DonorID, CollectionType) 
VALUES
	(1, '2021-10-25', 1, 'Whole Blood'),
	(2, '2021-10-15', 2, 'Plasma'),
	(3, '2021-08-20', 3, 'Platelets'),
	(4, '2021-09-30', 4, 'Whole Blood'),
	(5, '2021-10-05', 5, 'Whole Blood');

INSERT INTO Reports (ID, ReportType, CreationDate, ReportContent, ReportFile) 
VALUES
	(1, 'Medical Report', '2021-10-30', 'Patient is in good health.', NULL),
	(2, 'Blood Test Results', '2021-11-02', 'Cholesterol: 160 mg/dL', NULL),
	(3, 'Blood Test Results', '2021-10-05', 'Blood Pressure: 120/80 mmHg', NULL),
	(4, 'Blood Test Results', '2021-09-15', 'Cholesterol: 240 mg/dL', NULL),
	(5, 'Blood Test Results', '2021-10-20', 'Blood Pressure: 140/90 mmHg', NULL);
