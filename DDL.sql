SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;


CREATE OR REPLACE TABLE Residents
(
    residentID int UNIQUE AUTO_INCREMENT NOT NULL,
    residentName varchar(45) NOT NULL,
    birthDate DATE NOT NULL,
    allergyHistory varchar(225),
    diseaseHistory varchar(225),
    PRIMARY KEY (residentID)
);

CREATE OR REPLACE TABLE Vaccines
(
    vaccineID int UNIQUE AUTO_INCREMENT NOT NULL,
    targetDisease varchar(45) NOT NULL,
    vaccineType varchar(45) NOT NULL,
    vaccineManufacturer varchar(45) NOT NULL,
    PRIMARY KEY (vaccineID)
);

CREATE OR REPLACE TABLE Institutions
(
    institutionID int UNIQUE AUTO_INCREMENT NOT NULL,
    institutionName varchar(45) NOT NULL,
    publicInstituion BOOLEAN NOT NULL,
    PRIMARY KEY (institutionID)
);

CREATE OR REPLACE TABLE Records
(
    recordID int UNIQUE AUTO_INCREMENT NOT NULL,
    residentID int NOT NULL,
    vaccineID int NOT NULL,
    institutionID int,
    inoculationDate DATE NOT NULL,
    doseCount int NOT NULL,
    PRIMARY KEY (recordID),
    FOREIGN KEY (residentID) REFERENCES Residents(residentID) ON DELETE CASCADE,
    FOREIGN KEY (vaccineID) REFERENCES Vaccines(vaccineID) ON DELETE CASCADE,
    FOREIGN KEY (institutionID) REFERENCES Institutions(institutionID) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE Inventories
(
    vaccineID int NOT NULL,
    institutionID int NOT NULL,
    FOREIGN KEY (vaccineID) REFERENCES Vaccines(vaccineID) ON DELETE CASCADE,
    FOREIGN KEY (institutionID) REFERENCES Institutions(institutionID) ON DELETE CASCADE
);

INSERT INTO Residents
(
    residentName,
    birthDate,
    allergyHistory,
    diseaseHistory
)
VALUES
(
    "Pihla Amilcare",
    "2000-01-02",
    NULL,
    NULL
),
(
    "Nadezhda Gadise",
    "1943-04-29",
    "Amoxicillin",
    "Hip fracture"
),
(
    "Amar Klaas",
    "1983-11-11",
    "Cephalosporin",
    "Type II diabete"
);

INSERT INTO Vaccines
(
    targetDisease,
    vaccineType,
    vaccineManufacturer
)
VALUES
(
    "Varicella",
    "Inactivated",
    "Merck"
),
(
    "Typhoid",
    "Inactivated",
    "PaxVax"
),
(
    "Tetanus, (reduced) Diphtheria, (reduced) Pertussis",
    "Inactivated",
    "Sanofi"
),
(
    "Tetanus, (reduced) Diphtheria, (reduced) Pertussis",
    "Inactivated",
    "Merck"
),
(
    "Tetanus, (reduced) Diphtheria, (reduced) Pertussis",
    "Inactivated",
    "PaxVax"
);

INSERT INTO Institutions
(
    institutionName,
    publicInstituion
)
VALUES
(
    "YouNameIt",
    1
),
(
    "Whatever",
    1
),
(
    "Okay",
    0
);

INSERT INTO Records
(
    residentID,
    vaccineID,
    institutionID,
    inoculationDate,
    doseCount
)
VALUES
(
    (SELECT residentID FROM Residents WHERE residentID = 3),
    (SELECT vaccineID FROM Vaccines WHERE vaccineID = 3),
    (SELECT institutionID FROM Institutions WHERE institutionID = 3),
    "2001-02-03",
    2
),
(
    (SELECT residentID FROM Residents WHERE residentID = 2),
    (SELECT vaccineID FROM Vaccines WHERE vaccineID = 1),
    (SELECT institutionID FROM Institutions WHERE institutionID = 2),
    "2022-04-28",
    1
),
(
    (SELECT residentID FROM Residents WHERE residentID = 1),
    (SELECT vaccineID FROM Vaccines WHERE vaccineID = 2),
    (SELECT institutionID FROM Institutions WHERE institutionID = 1),
    "1988-05-11",
    1
);

INSERT INTO Inventories
(
    institutionID,
    vaccineID
)
VALUES
(
    (SELECT institutionID FROM Institutions WHERE institutionID = 1),
    (SELECT vaccineID FROM Vaccines WHERE vaccineID = 2)
),
(
    (SELECT institutionID FROM Institutions WHERE institutionID = 2),
    (SELECT vaccineID FROM Vaccines WHERE vaccineID = 1)
),
(
    (SELECT institutionID FROM Institutions WHERE institutionID = 3),
    (SELECT vaccineID FROM Vaccines WHERE vaccineID = 3)
);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;
