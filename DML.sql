-- Read information from resident you input
SELECT residentName, birthDate, allergyHistory, diseaseHistory FROM Residents;
WHERE residentID = :residentIDInput;

-- Create a new resident
INSERT INTO Residents
(
    residentName, birthDate, allergyHistory, diseaseHistory
)
VALUES
(
    :residentNameInput, :birthDateInput, :allergyHistoryInput, :diseaseHistoryInput
);

-- Update the chosen resident information
UPDATE Residents
SET residentName   = :residentNameInput,
    birthDate      = :birthDateInput,
    allergyHistory = :allergyHistoryInput,
    diseaseHistory = :diseaseHistoryInput
WHERE residentID   = :residentIDInput;

-- Delete the data of an exact resident
DELETE FROM Residents
WHERE residentID = :residentIDInput;


-- Read all vaccines' information
SELECT targetDisease, vaccineType, vaccineManufacturer FROM Vaccines;
-- Read all vaccines' information from the input institution
SELECT Vaccines.targetDisease, Vaccines.vaccineType, Vaccines.vaccineManufacturer FROM Vaccines
    JOIN Inventories ON (Vaccines.vaccineID = Inventories.vaccineID)
    JOIN Institutions ON (Inventories.institutionID = Institutions.institutionID)
    AND
    (Institutions.institutionID = :institutionIDInput);

-- Create a new vaccine
INSERT INTO Vaccines
(
    targetDisease, vaccineType, vaccineManufacturer
)
VALUES
(
    :targetDiseaseInput, :vaccineTypeInput, :vaccineManufacturerInput
);

-- Update the information of a chosen vaccine
UPDATE Vaccines
SET targetDisease       = :targetDiseaseInput,
    vaccineType         = :vaccineTypeInput,
    vaccineManufacturer = :vaccineManufacturerInput
WHERE vaccineID         = :vaccineIDInput;

-- Delete the data of an exact vaccine
DELETE FROM Vaccines
WHERE vaccineID = :vaccineIDInput;


-- Read all institutions' information
SELECT institutionID, institutionName, (CASE WHEN publicInstituion = 1 THEN 'Yes' ELSE 'No' END) AS Public FROM Institutions WHERE institutionID>0;

-- Create a new institution
INSERT INTO Institutions
(
    institutionName, publicInstituion
)
VALUES
(
    :institutionNameInput, :publicInstituionInput
);


-- Read all records' information
SELECT Records.recordID, Residents.residentName, Vaccines.targetDisease, Vaccines.vaccineManufacturer, Institutions.institutionName, Records.inoculationDate, Records.doseCount FROM Records JOIN Residents ON Records.residentID = Residents.residentID JOIN Vaccines ON Records.vaccineID = Vaccines.vaccineID JOIN Institutions on Records.institutionID = Institutions.institutionID ORDER BY Records.recordID;

-- Create a new record based on the table Residents, Vaccines, and Institutions
INSERT INTO Records
(
    residentID, vaccineID, institutionID, inoculationDate, doseCount
)
VALUES
(
    (SELECT residentID FROM Residents WHERE residentID = :residentIDInput),
    (SELECT vaccineID FROM Vaccines WHERE vaccineID = :vaccineIDInput),
    (SELECT institutionID FROM Institutions WHERE institutionID = :institutionIDInput),
    :inoculationDateInput, :doseCountInput
);

-- Update the information of a chosen record
DELETE FROM Records WHERE recordID = '%s'

INSERT INTO Records 
(
    residentID, vaccineID, institutionID, inoculationDate, doseCount
) 
VALUES 
(
    (SELECT residentID FROM Residents WHERE residentName = %s),
    (SELECT vaccineID FROM Vaccines WHERE targetDisease = %s and vaccineManufacturer = %s), 
    (SELECT institutionID FROM Institutions WHERE institutionName = %s), 
    %s, %s
);

-- Update the information of a chosen inventory
DELETE FROM Inventories 
WHERE institutionID = :institutionIDInput and vaccineID = :vaccineIDInput LIMIT 1;

INSERT INTO Inventories 
(
    institutionID, vaccineID
) 
VALUES 
(
    (SELECT institutionID FROM Institutions WHERE institutionName = %s),
    (SELECT vaccineID FROM Vaccines WHERE targetDisease = %s and vaccineManufacturer = %s)
);

-- Delete the data of an exact record
DELETE FROM Records
WHERE recordID = :recordIDInput;


-- Read the intersection table Inventories
SELECT institutionID, vaccineID FROM Inventories;

-- Create new relationship records between Institutions and Vaccines
INSERT INTO Inventories
(
    institutionID, vaccineID
)
VALUES
(
    (SELECT institutionID FROM Institutions WHERE institutionName = :institutionNameInput),
    (SELECT vaccineID FROM Vaccines WHERE targetDisease = :targetDiseaseInput and vaccineManufacturer=:vaccineManufacturerInput)
);

-- Delete the relationship of a pair of exact data between Institution and Vaccine
DELETE FROM Inventories 
WHERE institutionID = :institutionIDInput and vaccineID = :vaccineIDInput LIMIT 1;
