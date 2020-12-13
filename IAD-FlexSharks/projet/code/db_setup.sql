CREATE TABLE users(
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	email TEXT UNIQUE NOT NULL,
	name TEXT NOT NULL, -- (technically not useful in this demo)
	surname TEXT NOT NULL, -- (technically not useful in this demo)
	passwd TEXT NOT NULL -- hashed password (technically not useful in this demo)
);

CREATE TABLE flights(
	id INTEGER PRIMARY KEY AUTOINCREMENT,  
	dep_code TEXT NOT NULL, -- IATA code
	arr_code TEXT NOT NULL, -- IATA code
	dep_time INT NOT NULL, -- stored as UNIX epoch
	flight_number TEXT NOT NULL, -- not unique because flight numbers are the same every day (technically not useful in this demo)
	company_id INT NOT NULL -- (technically not useful in this demo)
); 

CREATE TABLE tickets(
	ticket_id INTEGER PRIMARY KEY AUTOINCREMENT, 
	buyer_id INTEGER REFERENCES users(id), -- can be NULL as long as the ticket isn't bought by someone
	flight_id INTEGER NOT NULL REFERENCES flights(id), 
	price REAL NOT NULL,
	seat TEXT NOT NULL, -- (technically not useful in this demo)
	UNIQUE (buyer_id, flight_id, price, seat), 
	CHECK(typeof(ticket_id)='integer') -- "dynamic typing"... really ? https://dba.stackexchange.com/questions/106364/text-string-stored-in-sqlite-integer-column
	CHECK(typeof(buyer_id)='integer' OR buyer_id IS NULL)
	CHECK(typeof(flight_id)='integer')
	FOREIGN KEY(buyer_id) REFERENCES users(id),
	FOREIGN KEY(flight_id) REFERENCES flights(id)
	-- TODO flights available count ?
);

PRAGMA foreign_keys = ON; -- enable foreign keys in SQLite
