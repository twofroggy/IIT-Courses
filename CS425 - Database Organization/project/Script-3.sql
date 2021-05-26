drop view if exists W2; 

drop view if exists expenseReportTotal;  
drop view if exists expenseReport;  

drop view if exists biweekly_paycheck; 
drop view if exists paycheck; 

DROP TABLE IF EXISTS Federal;
DROP TABLE IF EXISTS State;
DROP TABLE IF EXISTS Social_Security;
DROP TABLE IF EXISTS Benefits;
DROP TABLE IF EXISTS Dependents;
DROP TABLE IF EXISTS Insurance;
DROP TABLE IF EXISTS Health_Benefits;
DROP TABLE IF EXISTS Benefit_401k;
DROP TABLE IF EXISTS Bonus; 
drop table if exists Medicare; 
DROP TABLE IF EXISTS Employee cascade; 

CREATE TABLE Employee ( 
	firstName VARCHAR(20), 
	lastName VARCHAR(20), 
	address VARCHAR(20), 
	jobTitle VARCHAR(20), 
	salaryType VARCHAR(20),
    hoursWorked INT,
	salary INT, 
	SSN VARCHAR(11), 
	username VARCHAR(20) not null unique,
	user_password VARCHAR(20) not null, 
	PRIMARY key (SSN) 
);

CREATE INDEX employeeSSN 
ON Employee(SSN);

CREATE TABLE Federal ( 
  taxRate FLOAT(20), 
  bracket VARCHAR(20), 
  SSN VARCHAR (11), 
  FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
  );

CREATE TABLE Medicare ( 
	rate FLOAT (20), 
	SSN VARCHAR(11), 
	FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
);

CREATE TABLE State( 
  stateName VARCHAR(20), 
  stateTaxRate FLOAT(20), 
  SSN VARCHAR(11), 
  FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
 );

CREATE TABLE Social_Security( 
	totalPercent FLOAT(20), 
	employeePercent FLOAT(20), 
	employerPercent FLOAT(20), 
	SSN VARCHAR(11), 
	FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
);

CREATE TABLE Benefits( 
	healthPlan VARCHAR (20), 
	attorneyPlan VARCHAR (20), 
	SSN VARCHAR (11), 
	FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
);

CREATE TABLE Dependents( 
	full_name VARCHAR (20), 
	dependent_SSN VARCHAR(11) not null, 
	relationship VARCHAR(25), 
	SSN VARCHAR(11) not null, 
	FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
); 

CREATE INDEX DependentsSSN 
ON Dependents(dependent_SSN);

CREATE TABLE Insurance( 
	insurancePlan VARCHAR (25), 
	individualCost FLOAT (20), 
	familyCost FLOAT (20), 
	employeeContribution_ins DECIMAL (5, 2), 
	employerContribution_ins DECIMAL (5, 2), 
	SSN VARCHAR (11), 
	FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
);

CREATE TABLE Health_Benefits( 
	dentalInsurance VARCHAR(20), 
	visionInsurance VARCHAR(20), 
	lifeInsurance VARCHAR(20), 
	SSN VARCHAR(11), 
	FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
);

CREATE TABLE Benefit_401k( 
	employeeContribution_ben DECIMAL(5, 2), 
	employerContribution_ben DECIMAL(5, 2), 
	SSN VARCHAR(11), 
	FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
);

CREATE TABLE Bonus( 
	employeePerformance FLOAT(20),    
	companyPercent FLOAT(20),  
	SSN VARCHAR(11), 
	FOREIGN key (SSN) REFERENCES Employee(SSN) on delete cascade
);

create view expenseReport AS
select 
username, 
SSN, 
salary, 
employeePerformance*companyPercent*salary as bonus, 
employerContribution_ben*salary as employer_contribution_amount,
social_security.employerPercent*salary as social_security_amount,
Insurance.employerContribution_ins * salary as insurance_amount
FROM 
Employee natural join 
Bonus natural join 
Benefit_401k natural join 
Social_Security natural join 
Insurance;

create view expenseReportTotal AS
select SUM(salary) as salary, 
SUM(bonus) as bonus, 
SUM(employer_contribution_amount) as employer_contribution_amount, 
SUM(social_security_amount)as social_security_amount,
SUM(insurance_amount) as insurance_amount
FROM expenseReport;




create view  W2 as (
select 
username,
SSN, 
salary, 
employeePerformance*companyPercent*salary as bonus, 
(medicare.rate*salary + state.stateTaxRate*salary + Federal.taxRate*salary + Social_Security.employeePercent*salary + Benefit_401k.employeeContribution_ben*salary +  Insurance.individualCost + Insurance.familyCost) as deduction

from 
Employee natural join 
bonus natural join 
Medicare natural join 
State natural join 
Federal natural join 
Benefit_401k natural join 
Social_Security natural join 
Insurance
); 


create view paycheck AS
SELECT e.username, e.SSN, e.salary, 
CASE
	WHEN hoursWorked IS NULL THEN e.salary
	ELSE hoursWorked*e.salary
	END AS totalSalary, 
case 
	when hoursWorked is not null then 0
	ELSE employeePerformance*companyPercent*salary 
    end as bonus, 
m.rate*e.salary as medicare_amount, 
s.stateTaxRate*e.salary as state_tax_amount, 
f.taxRate*e.salary as federal_tax_amount, 
y.employeePercent*e.salary as social_security_amount, 
t.employeeContribution_ben*e.salary as employee_401k_contribution, 
i.individualCost + i.familyCost  as insurance_cost
FROM
Employee e 
inner join Medicare m on e.SSN = m.SSN 
inner join State s on e.SSN = s.SSN 
inner join Federal f on e.SSN = f.SSN 
inner join Benefit_401k t on e.SSN = t.SSN  
inner join Social_Security y on e.SSN = y.SSN 
inner join Insurance i on e.SSN = i.SSN 
inner join Bonus b on e.SSN = b.SSN; 

create view biweekly_paycheck AS
SELECT username, SSN,
CASE
	WHEN employee.salaryType='hourly' THEN hoursWorked*salary
	ELSE salary/26
	end as BiweeklySalary,
bonus/26 as bonus,medicare_amount, state_tax_amount, federal_tax_amount, social_security_amount,
employee_401k_contribution,insurance_cost
from employee natural join paycheck; 


insert into Employee ( firstName, lastName, address, jobTitle, salaryType , hoursWorked, salary, SSN, username, user_password) 
values ('Tiffany', 'Wong', '123 lane', 'employee', 'hourly', 15, 21, '123-45-6789', 'twong', 't');
insert into Employee ( firstName, lastName, address, jobTitle, salaryType ,salary, SSN, username, user_password) 
values	('Alisha', 'Khan', '213 park', 'manager', 'annual', 80000, '213-45-6789', 'akhan', 'a'), 
        ('Neveen', 'Elmajdoub', '312 route', 'admin', 'annual', 60000, '312-45-6789', 'nelmajdoub', 'n');

insert into Federal(taxRate, bracket, SSN)
values (0.02,'bracket1', '123-45-6789'),
       (0.02,'bracket2', '213-45-6789'),
       (0.02,'bracket3', '312-45-6789');
       
insert into Medicare (rate, SSN)
values (0.12,'123-45-6789'),
       (0.12,'213-45-6789'),
       (0.12, '312-45-6789');
       
insert into State(stateName, stateTaxRate, SSN)
values ('California',0.05,'123-45-6789'),
       ('Illinois',0.05,'213-45-6789'),
       ('New York',0.05, '312-45-6789');

insert into Social_Security(totalPercent, employeePercent, employerPercent, SSN)
values (0.15,0.15,0,'123-45-6789'),
       (0.15,0.075,0.075,'312-45-6789'),
       (0.15,0.075,0.075, '213-45-6789');

insert into Benefits(healthPlan, attorneyPlan, SSN)
values ('health plan1','attorney plan1','123-45-6789'),
       ('health plan2','attorney plan2','213-45-6789'),
       ('health plan3','attorney plan3', '312-45-6789');

insert into Dependents(full_name, dependent_SSN, relationship, SSN)
values ('wong1','223-45-6789','sister','123-45-6789'),
       ('khan1','313-45-6789','daughter','213-45-6789'),
       ('khan2','413-45-6789','daughter','213-45-6789'),
       ('neveen1','412-45-6789','son', '312-45-6789');
       
insert into Insurance (insurancePlan, individualCost, familyCost, employeeContribution_ins,employerContribution_ins,SSN)
values ('plan1',100,200,0.90,0.1,'123-45-6789'),
       ('plan2',300,400,0.80,0.2,'213-45-6789'),
       ('plan3',500,600,0.7,0.3,'312-45-6789');
       
insert into Health_Benefits(dentalInsurance,visionInsurance,lifeInsurance,SSN)
values ('d1','v1','l1','123-45-6789'),
       ('d2','v2','l2','213-45-6789'),
       ('d3','v3','l3','312-45-6789');


insert into Benefit_401k(employeeContribution_ben, employerContribution_ben, SSN)
values (0.90,0.1,'123-45-6789'),
       (0.80,0.2,'213-45-6789'),
       (0.6,0.4,'312-45-6789');


insert into Bonus(employeePerformance,companyPercent,SSN)
values (0,1.5,'123-45-6789'),
       (1.5,1.5,'312-45-6789'), 
       (1,1.5, '213-45-6789');
      
select * 
from employee natural join bonus
where SSN = '123-45-6789'; 


select * 
from paycheck 
where SSN = '123-45-6789'; 

update Benefit_401k 
set employeeContribution_ben = '2' 
where SSN = '123-45-6789'; 

select *
from  W2 
where SSN = '123-45-6789'; 

select * 
from employee ; 

select * from state ;

select * from biweekly_paycheck;

select* from benefit_401k bk ;

select * from expenseReportTotal;