<<<<<<< HEAD
-- Stations (Parent Table)
CREATE TABLE stations (
    station_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    contact_number TEXT,
    website TEXT,
    address TEXT,
    city_id INTEGER,
    status_id INTEGER,
    parent_company_id INTEGER
);

-- Station SPOCs (Contact Points)
CREATE TABLE station_spocs (
    spoc_id INTEGER PRIMARY KEY,
    station_id INTEGER REFERENCES stations(station_id),
    name TEXT,
    email TEXT,
    designation TEXT
);

-- Problem Banks
CREATE TABLE problem_banks (
    problem_bank_id INTEGER PRIMARY KEY,
    station_id INTEGER REFERENCES stations(station_id),
    business_domain TEXT,
    total_requirements INTEGER,
    batch_id INTEGER
);

-- Projects (Main Entity)
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    station_id INTEGER REFERENCES stations(station_id),
    problem_bank_id INTEGER REFERENCES problem_banks(problem_bank_id),
    title TEXT,
    description TEXT,
    mentor_name TEXT,
    created_by TEXT
);

-- Project Skills (Many-to-Many)
CREATE TABLE project_skills (
    project_id INTEGER REFERENCES projects(project_id),
    skill_id INTEGER,
    PRIMARY KEY (project_id, skill_id)
);

-- Project Facilities
CREATE TABLE project_facilities (
    facility_id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(project_id),
    stipend REAL,
    currency TEXT,
    office_hours TEXT
=======
-- Stations (Parent Table)
CREATE TABLE stations (
    station_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    contact_number TEXT,
    website TEXT,
    address TEXT,
    city_id INTEGER,
    status_id INTEGER,
    parent_company_id INTEGER
);

-- Station SPOCs (Contact Points)
CREATE TABLE station_spocs (
    spoc_id INTEGER PRIMARY KEY,
    station_id INTEGER REFERENCES stations(station_id),
    name TEXT,
    email TEXT,
    designation TEXT
);

-- Problem Banks
CREATE TABLE problem_banks (
    problem_bank_id INTEGER PRIMARY KEY,
    station_id INTEGER REFERENCES stations(station_id),
    business_domain TEXT,
    total_requirements INTEGER,
    batch_id INTEGER
);

-- Projects (Main Entity)
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    station_id INTEGER REFERENCES stations(station_id),
    problem_bank_id INTEGER REFERENCES problem_banks(problem_bank_id),
    title TEXT,
    description TEXT,
    mentor_name TEXT,
    created_by TEXT
);

-- Project Skills (Many-to-Many)
CREATE TABLE project_skills (
    project_id INTEGER REFERENCES projects(project_id),
    skill_id INTEGER,
    PRIMARY KEY (project_id, skill_id)
);

-- Project Facilities
CREATE TABLE project_facilities (
    facility_id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(project_id),
    stipend REAL,
    currency TEXT,
    office_hours TEXT
>>>>>>> bf2110df8bb1623be4b7b45140e00ae579b78634
);