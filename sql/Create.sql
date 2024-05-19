CREATE TABLE donors
(
    id                   SERIAL PRIMARY KEY,
    first_name           VARCHAR(50) NOT NULL,
    last_name            VARCHAR(50) NOT NULL,
    middle_name          VARCHAR(50),
    date_of_birth        DATE        NOT NULL,
    gender               VARCHAR(10) NOT NULL,
    address              VARCHAR(255),
    phone_number         VARCHAR(20),
    hospital_affiliation VARCHAR(255),
    passport_data        VARCHAR(50),
    insurance_data       VARCHAR(50),
    blood_type           VARCHAR(5)  NOT NULL,
    rh_factor            VARCHAR(5)  NOT NULL
);

CREATE TABLE medicalhistory
(
    id                    SERIAL PRIMARY KEY,
    donor_id              INT     NOT NULL,
    last_examination_date DATE    NOT NULL,
    test_results          VARCHAR(255),
    donation_ban          BOOLEAN NOT NULL,
    CONSTRAINT FK_DonorID_MedicalHistory FOREIGN KEY (donor_id) REFERENCES donors (id)
);

CREATE TABLE bloodcollections
(
    id              SERIAL PRIMARY KEY,
    collection_date DATE        NOT NULL,
    donor_id        INT         NOT NULL,
    collection_type VARCHAR(50) NOT NULL,
    CONSTRAINT FK_DonorID_BloodCollections FOREIGN KEY (donor_id) REFERENCES donors (id)
);

CREATE TABLE reports
(
    id             SERIAL PRIMARY KEY,
    report_type    VARCHAR(50) NOT NULL,
    creation_date  DATE        NOT NULL,
    report_content TEXT,
    report_file    BYTEA
);

CREATE TABLE doctors
(
    id         SERIAL PRIMARY KEY,
    first_name VARCHAR(50)        NOT NULL,
    last_name  VARCHAR(50)        NOT NULL,
    position   VARCHAR(50)        NOT NULL,
    login      VARCHAR(50) UNIQUE NOT NULL,
    password   VARCHAR(50)        NOT NULL,
    email      VARCHAR(50)
);