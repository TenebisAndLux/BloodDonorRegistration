INSERT INTO donors (first_name, last_name, middle_name, date_of_birth, gender, address, phone_number,
                    hospital_affiliation,
                    passport_data, insurance_data, blood_type, rh_factor)
VALUES ('John', 'Doe', 'l', '1990-05-15', 'M', '123 Main St', '555-1234', 'St. Mary Hospital', 'ABC123456',
        'Some Insurance Company', 'A', '+'),
       ('Jane', 'Doe', 'x', '1985-06-20', 'F', '456 Oak St', '555-9876', 'St. John Hospital', 'CD123456',
        'Another Insurance Company', 'B', '-'),
       ('Jack', 'Smith', NULL, '1975-07-10', 'M', '789 Maple St', '555-5678', 'St. Mary Hospital', 'EF123456',
        'Some Insurance Company', 'AB', '+'),
       ('Jill', 'Smith', 'y', '1995-12-05', 'F', '321 Elm St', '555-1472', 'St. John Hospital', 'GH123456',
        'Another Insurance Company', 'A', '-'),
       ('James', 'Johnson', 'z', '1980-08-15', 'M', '951 Oak Ave', '555-9012', 'St. Mary Hospital', 'IJ123456',
        'Some Insurance Company', 'O', '+');

INSERT INTO bloodcollections (collection_date, donor_id, collection_type)
VALUES ('2020-01-05', 1, 'Whole Blood'),
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

INSERT INTO reports (report_type, creation_date, report_content, report_file)
VALUES ('Medical Report', '2020-01-05', 'Patient is in good health.', NULL),
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

INSERT INTO doctors (first_name, last_name, position, login, password, email)
VALUES ('John', 'Doe', 'Doctor', 'johndoe', '123', 'johndoe@gmail.com'),
       ('Jane', 'Smith', 'Nurse', 'janesmith', '123', 'janesmith@gmail.com'),
       ('Jack', 'Johnson', 'Surgeon', 'jackjohnson', '123', 'jackjohnson@gmail.com'),
       ('Jill', 'Williams', 'Doctor', 'jillwilliams', '123', 'jillwilliams@gmail.com'),
       ('James', 'Brown', 'Nurse', 'jamesbrown', '123', 'jamesbrown@gmail.com');

INSERT INTO medicalhistory (donor_id, last_examination_date, test_results, donation_ban)
VALUES (1, '2021-10-20', 'Normal', FALSE),
       (2, '2021-09-10', 'Normal', FALSE),
       (3, '2021-07-15', 'Elevated cholesterol', TRUE),
       (4, '2021-10-10', 'Normal', FALSE),
       (5, '2021-09-05', 'Elevated blood pressure', TRUE);
