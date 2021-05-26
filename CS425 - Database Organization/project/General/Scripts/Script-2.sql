
DROP TABLE IF EXISTS Federal;
DROP TABLE IF EXISTS State;
DROP TABLE IF EXISTS Social_Security;
DROP TABLE IF EXISTS Benefits;
DROP TABLE IF EXISTS Dependents;
DROP TABLE IF EXISTS Insurance;
DROP TABLE IF EXISTS Health_Benefits;
DROP TABLE IF EXISTS Benefit_401k;
DROP TABLE IF EXISTS Bonus;
DROP TABLE IF EXISTS Employee CASCADE; 

CREATE TABLE Employee ( firstName VARCHAR(20), lastName VARCHAR(20), jobTitle VARCHAR(20), salaryType VARCHAR(20), salary INT, SSN VARCHAR(11), PRIMARY key (SSN) );

CREATE INDEX employeeSSN 
ON Employee(SSN);

CREATE TABLE Federal ( taxRate FLOAT(20), bracket VARCHAR(20) SSN VARCHAR (11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

CREATE TABLE Medicare ( rate FLOAT (20), SSN VARCHAR(11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

CREATE TABLE State( stateName VARCHAR(20), stateTaxRate FLOAT(20) SSN VARCHAR(11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

CREATE TABLE Social_Security( totalPercent FLOAT(20), employeePercent FLOAT(20), employerPercent FLOAT(20), SSN VARCHAR(11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

CREATE TABLE Benefits( healthPlan VARCHAR (20), attorneyPlan VARCHAR (20), SSN VARCHAR (11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

CREATE TABLE Dependents( name VARCHAR (20), dependent_SSN VARCHAR(11), relationship VARCHAR(25), SSN VARCHAR(11), FOREIGN key (SSN) REFERENCES Employee(SSN) );
CREATE INDEX DependentsSSN 
ON Dependents(dependent_SSN);

CREATE TABLE Insurance( insurancePlan VARCHAR (25), individualCost FLOAT (20), familyCost FLOAT (20), employeeContribution DECIMAL (5, 2), employerContribution DECIMAL (5, 2), SSN VARCHAR (11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

CREATE TABLE Health_Benefits( dentalInsurance VARCHAR(20), visionInsurance VARCHAR(20), lifeInsurance VARCHAR(20), SSN VARCHAR(11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

CREATE TABLE Benefit_401k( maxMatch FLOAT(20), employeeContribution DECIMAL(5, 2), employerContribution DECIMAL(5, 2), SSN VARCHAR(11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

CREATE TABLE Bonus( employeePerformance FLOAT(20), maxPercent FLOAT(20), SSN VARCHAR(11), FOREIGN key (SSN) REFERENCES Employee(SSN) );

