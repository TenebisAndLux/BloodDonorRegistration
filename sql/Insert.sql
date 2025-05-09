-- Вставка в MedicalInstitution
INSERT INTO MedicalInstitution (NameOfInstitution, Address, ContactPhoneNumber, Email, TypeOfInstitution) VALUES
('Центр крови №1', 'Москва, ул. Красная, д.1', '+74951234567', 'blood1@example.com', 'Городской центр крови'),
('Центр крови №2', 'Санкт-Петербург, Невский пр-т, д.10', '+78121234567', 'blood2@example.com', 'Областной центр крови');

-- Вставка в Doctor
INSERT INTO Doctor (InstitutionCode, ServiceNumber, Role, Name, SecondName, JobTitle, Login, Password, Email) VALUES
(1, 101, 'doctor', 'Иван', 'Петров', 'Трансфузиолог', 'ipetrov', 'scrypt:32768:8:1$K3KAgb4z5Qe5hyFU$34e84a5a1a113326f9270e66ee6f7b5a2b84afc60d162cca829ec6dc54133065c452154d74e72e120ad6fe40f891fbd6a7f10c17c1c4cb71cbeb4277eeb7ff6f', 'ipetrov@example.com'),
(1, 102, 'doctor','Мария', 'Сидорова', 'Гематолог', 'msidorova', 'scrypt:32768:8:1$RozEUXluUs1wJQG8$a2ad3e74e58b92d5cf015d5e912a86dc656027b7b9e7953e11ce3d8e6ef5419524b1ae3b8e64f8825cbc80a3b70e533dc803312e00cf58e970813c7fb15b275a', 'msidorova@example.com'),
(2, 201, 'admin','Алексей', 'Смирнов', 'Терапевт', 'asmirnov', 'scrypt:32768:8:1$zlWTgj5794AlM5Np$b3545e42be3b2f886cf367a404155c02c21c978cf9c44e0c6f1f8723c28b8140596f48ca184fbe2ab1cf659691e05e0ba03e932c622238e77786ef7e3596ec51', 'asmirnov@example.com'),
(2, 202, 'doctor','Ольга', 'Иванова', 'Иммунолог', 'oivanova', 'scrypt:32768:8:1$drl9rzecYKI23E0s$60e13f193817acccbd9c987c2afe551fed2114ef69066bcbf5dbd06f4eacd3d325f465d5cf402a151fc730558b3538647d577b7c04464912fef1688e54d8f4d9', 'oivanova@example.com');

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
