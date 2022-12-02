# Vaccination-DB

_Overview_
Vaccination DB is a database that records local vaccination information. It is a database created jointly by local institutions and used to provide residents with clearer information about vaccines. In this neighborhood, there are 1300 residents, 8 vaccination institutions, and 21 vaccines. This also means that up to 30,000 vaccination records need to be stored. A database-driven website will provide basic information on vaccines and vaccination institutions. It will also store basic resident information and vaccination records.

A total of 4 basic entities will be created in the database, including Residents, Vaccines, Institutions, and Records. Each of these entities, according to their names, will be reasonable for recording the corresponding data. The connection table Inventories connecting two entities as an adjunct to the M:N relationship for vaccines and institutions.

_Database Outline_

Residents: information of residents, including names, dates of birth and medical histories. 
1:M relationship between Residents and Records, with residentID as FK inside Records.
residentID: INT, unique, auto increment, not NULL, PK
residentName: varchar(45), not NULL
birthDate: DATE, not NULL
allergyHistory: varchar(225)
diseaseHistory: varchar(225)

Vaccines: information of vaccines, including types, uses and manufacturers.
1:1 relationship between Vaccines and Records, with vaccineID as FK inside Records.
M:N relationship between Vaccines and Institutions, with a connecting table Inventories which takes as FK.
vaccineID: INT, unique, auto increment, not NULL, PK
targetDisease: varchar(45), not NULL
vaccineType: varchar(45), not NULL
vaccineManufacturer: varchar(45), not NULL

Institutions: information of institutions, including name and properties.
M:N relationship between Institutions and Vaccines, with a connecting table Inventories which takes vaccineID as FK.
1:M relationship between Institutions and Records, with institutionID as FK inside Records.
institutionID: INT, unique, auto increment, not NULL, PK
institutionName: varchar(45), not NULL
publicInstitution: BOOLEAN, not NULL

Records: records of inoculation.
M:1 relationship between Records and Residents, with residentID as FK inside Records 1:1 relationship between Records and Vaccines, with vaccineID as FK inside Records.
M:1 relationship between Records and Institutions, with institutionID as FK inside Records.
recordID: INT, unique, auto increment, not NULL, PK
residentID: INT, not NULL, FK
vaccineID: INT, not NULL, FK
institutionID: INT, not NULL, FK
inoculationDate: DATE, not NULL
doseCount: INT, not NULL

Inventories: Connecting Table for Institutions & Vaccines.
1:M relationship between inventories and Institutions, with institutionID as FK inside inventories 1:M relationship between inventories and Vaccines, with vaccineID as FK inside inventories.
institutionID: INT, not NULL, FK
vaccineID: INT, not NULL, FK
