drop table if exists booking; 
drop table if exists flight; 
drop table if exists customer; 
drop table if exists airport; 
drop table if exists agent; 

create table agent 
( 
	agentName varchar NOT NULL, 
	price int NOT NULL, 
	phone bigint NOT NULL 
		constraint agent_pk 
			primary key 
);
	
CREATE table airport( 
	IATA varchar 
		constraint airport_pk 
			primary key, 
	city varchar, 
	airportType varchar
	); 
	
CREATE table flight ( 
	airlineCode varchar NOT NULL, 
	flightNumber int NOT NULL, 
	price int, 
	seat int, 
	IATA varchar, 
	IATALands varchar, 
	timeDep time NOT NULL, 
	timeArr time NOT NULL, 
	flightDate varchar NOT NULL, 
	constraint flight_pk
		unique (flightNumber, airlineCode, flightDate)
			primary key
); 

CREATE table customer ( 
	phone bigint NOT NULL 
		constraint customer_pk
			primary key, 
	customerName varchar NOT NULL, 
	agentName varchar NOT NULL, 
	constraint customer_agent_agentname_fk
			references agent 
	); 

create table booking ( 
	phone bigint NOT NULL
        constraint booking_customer_phone_fk
            references customer,
    flightNumber int NOT NULL,
    airlineCode varchar NOT NULL,
    flightDate varchar NOT NULL,
    seat varchar NOT NULL,
    price int NOT NULL,
    agentName varchar NOT NULL,
    constraint booking_pk
        unique (phone, flightNumber, airlineCode, flightDate) 
        	primary key
);
	
create table user (
	userName varchar(15) NOT NULL 
		constraint user_pk
			primary key, 
	password varchar(20) NOT NULL, 
	phone int NOT NULL 
		constraint user_agentphone_fk
			references agent(phone), 
		constraint user_customerphone_fk
	email varchar(255) NOT NULL
		constraint emailcheck 
			check ((email)::text ~~ '_%@_'::text) 
			
)

	
	