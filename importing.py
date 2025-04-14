<<<<<<< HEAD
import sqlite3
import json
from datetime import datetime

# 1. Initialize DB
def create_db():
    conn = sqlite3.connect('station_data_v2.db')
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS stations (
            station_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_number TEXT,
            website TEXT,
            address TEXT,
            city_id INTEGER,
            status_id INTEGER,
            parent_company_id INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS station_spocs (
            spoc_id INTEGER,
            station_id INTEGER REFERENCES stations(station_id),
            name TEXT,
            email TEXT,
            designation TEXT,
            contact_number TEXT,
            PRIMARY KEY (spoc_id, station_id)
        );
        
        CREATE TABLE IF NOT EXISTS problem_banks (
            problem_bank_id INTEGER PRIMARY KEY,
            station_id INTEGER REFERENCES stations(station_id),
            business_domain TEXT,
            total_requirements INTEGER,
            batch_id INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY,
            station_id INTEGER REFERENCES stations(station_id),
            problem_bank_id INTEGER REFERENCES problem_banks(problem_bank_id),
            title TEXT,
            description TEXT,
            mentor_name TEXT,
            created_by TEXT,
            mode TEXT
        );
        
        CREATE TABLE IF NOT EXISTS project_skills (
            project_id INTEGER REFERENCES projects(project_id),
            skill_id INTEGER,
            PRIMARY KEY (project_id, skill_id)
        );
        
        CREATE TABLE IF NOT EXISTS project_facilities (
            facility_id INTEGER PRIMARY KEY,
            project_id INTEGER REFERENCES projects(project_id),
            stipend REAL,
            currency TEXT,
            office_hours TEXT
        );
    ''')
    return conn

# 2. Import Data
def import_data(conn):
    with open('data.json') as f:
        json_data = json.load(f)
        if not json_data or 'data' not in json_data:
            print("Error: Invalid or empty data in data.json")
            return
        data = json_data['data']  # data is a dictionary with station IDs as keys
    
    cursor = conn.cursor()
    
    # OPTIMIZE FOR SPEED
    cursor.execute("PRAGMA journal_mode = MEMORY")
    cursor.execute("PRAGMA synchronous = OFF")
    
    # Insert Stations
    for station_id, station_data in data.items():
        if not isinstance(station_data, dict) or 'station_details' not in station_data:
            print(f"Warning: Invalid station data for ID {station_id}")
            continue
            
        station = station_data['station_details']
        cursor.execute('''
            INSERT INTO stations VALUES (?,?,?,?,?,?,?,?)
        ''', (
            station.get('stationId'),
            station.get('stationName'),
            station.get('stationContactNumber'),
            station.get('websiteAddress'),
            f"{station.get('address1', '')} {station.get('address2', '')}".strip(),
            station.get('cityId'),
            station.get('statusId'),
            station.get('parentCompanyId')
        ))
        
        # Insert SPOCs
        for spoc in station.get('stationSpocs', []):
            cursor.execute('''
                INSERT OR IGNORE INTO station_spocs VALUES (?,?,?,?,?,?)
            ''', (
                spoc.get('stationSpocId'),
                station.get('stationId'),
                spoc.get('name'),
                spoc.get('emailAddress'),
                spoc.get('designation'),
                spoc.get('contactNumber')
            ))
    
    # Insert Problem Banks and Projects
    for station_id, station_data in data.items():
        if not isinstance(station_data, dict):
            continue
            
        problem_banks = station_data.get('problem_banks', {}).get('problemBankGridLines', [])
        for pb in problem_banks:
            if not pb:
                continue
            cursor.execute('''
                INSERT OR IGNORE INTO problem_banks VALUES (?,?,?,?,?)
            ''', (
                pb.get('problemBankId'),
                pb.get('stationId'),
                pb.get('businessDomain'),
                pb.get('totalRequirement', 0),
                pb.get('batchId')
            ))
        
        projects = station_data.get('project_details', {})
        if not isinstance(projects, dict):
            continue
            
        for project_id, project in projects.items():
            if not project:
                continue
            # Get mode from projectFacility or default to Online
            project_facilities = project.get('projectFacility', [])
            mode = 'Online'  # Default mode
            if project_facilities and isinstance(project_facilities, list) and len(project_facilities) > 0:
                facility = project_facilities[0]
                if isinstance(facility, dict):
                    mode = facility.get('mode', 'Online')
            
            cursor.execute('''
                INSERT OR IGNORE INTO projects VALUES (?,?,?,?,?,?,?,?)
            ''', (
                project.get('projectId'),
                station_id,
                project.get('problemBankId'),
                project.get('title'),
                project.get('description'),
                project.get('mentorName'),
                project.get('createdBy'),
                mode
            ))
            
            # Skills
            for skill in project.get('projectSkill', []):
                if not skill:
                    continue
                cursor.execute('''
                    INSERT OR IGNORE INTO project_skills VALUES (?,?)
                ''', (
                    project.get('projectId'),
                    skill.get('skillId')
                ))
            
            # Facilities
            for facility in project.get('projectFacility', []):
                if not facility:
                    continue
                cursor.execute('''
                    INSERT OR IGNORE INTO project_facilities VALUES (?,?,?,?,?)
                ''', (
                    facility.get('projectFacilityId'),
                    project.get('projectId'),
                    facility.get('ugstipend', 0.0),
                    facility.get('currency'),
                    f"{facility.get('officeStartTime', '')}-{facility.get('officeEndTime', '')}"
                ))
    
    conn.commit()

if __name__ == "__main__":
    conn = create_db()
    import_data(conn)
    print("Database created: station_data.db")
=======
import sqlite3
import json
from datetime import datetime

# 1. Initialize DB
def create_db():
    conn = sqlite3.connect('station_data_v2.db')
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS stations (
            station_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_number TEXT,
            website TEXT,
            address TEXT,
            city_id INTEGER,
            status_id INTEGER,
            parent_company_id INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS station_spocs (
            spoc_id INTEGER,
            station_id INTEGER REFERENCES stations(station_id),
            name TEXT,
            email TEXT,
            designation TEXT,
            contact_number TEXT,
            PRIMARY KEY (spoc_id, station_id)
        );
        
        CREATE TABLE IF NOT EXISTS problem_banks (
            problem_bank_id INTEGER PRIMARY KEY,
            station_id INTEGER REFERENCES stations(station_id),
            business_domain TEXT,
            total_requirements INTEGER,
            batch_id INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY,
            station_id INTEGER REFERENCES stations(station_id),
            problem_bank_id INTEGER REFERENCES problem_banks(problem_bank_id),
            title TEXT,
            description TEXT,
            mentor_name TEXT,
            created_by TEXT,
            mode TEXT
        );
        
        CREATE TABLE IF NOT EXISTS project_skills (
            project_id INTEGER REFERENCES projects(project_id),
            skill_id INTEGER,
            PRIMARY KEY (project_id, skill_id)
        );
        
        CREATE TABLE IF NOT EXISTS project_facilities (
            facility_id INTEGER PRIMARY KEY,
            project_id INTEGER REFERENCES projects(project_id),
            stipend REAL,
            currency TEXT,
            office_hours TEXT
        );
    ''')
    return conn

# 2. Import Data
def import_data(conn):
    with open('data.json') as f:
        json_data = json.load(f)
        if not json_data or 'data' not in json_data:
            print("Error: Invalid or empty data in data.json")
            return
        data = json_data['data']  # data is a dictionary with station IDs as keys
    
    cursor = conn.cursor()
    
    # OPTIMIZE FOR SPEED
    cursor.execute("PRAGMA journal_mode = MEMORY")
    cursor.execute("PRAGMA synchronous = OFF")
    
    # Insert Stations
    for station_id, station_data in data.items():
        if not isinstance(station_data, dict) or 'station_details' not in station_data:
            print(f"Warning: Invalid station data for ID {station_id}")
            continue
            
        station = station_data['station_details']
        cursor.execute('''
            INSERT INTO stations VALUES (?,?,?,?,?,?,?,?)
        ''', (
            station.get('stationId'),
            station.get('stationName'),
            station.get('stationContactNumber'),
            station.get('websiteAddress'),
            f"{station.get('address1', '')} {station.get('address2', '')}".strip(),
            station.get('cityId'),
            station.get('statusId'),
            station.get('parentCompanyId')
        ))
        
        # Insert SPOCs
        for spoc in station.get('stationSpocs', []):
            cursor.execute('''
                INSERT OR IGNORE INTO station_spocs VALUES (?,?,?,?,?,?)
            ''', (
                spoc.get('stationSpocId'),
                station.get('stationId'),
                spoc.get('name'),
                spoc.get('emailAddress'),
                spoc.get('designation'),
                spoc.get('contactNumber')
            ))
    
    # Insert Problem Banks and Projects
    for station_id, station_data in data.items():
        if not isinstance(station_data, dict):
            continue
            
        problem_banks = station_data.get('problem_banks', {}).get('problemBankGridLines', [])
        for pb in problem_banks:
            if not pb:
                continue
            cursor.execute('''
                INSERT OR IGNORE INTO problem_banks VALUES (?,?,?,?,?)
            ''', (
                pb.get('problemBankId'),
                pb.get('stationId'),
                pb.get('businessDomain'),
                pb.get('totalRequirement', 0),
                pb.get('batchId')
            ))
        
        projects = station_data.get('project_details', {})
        if not isinstance(projects, dict):
            continue
            
        for project_id, project in projects.items():
            if not project:
                continue
            # Get mode from projectFacility or default to Online
            project_facilities = project.get('projectFacility', [])
            mode = 'Online'  # Default mode
            if project_facilities and isinstance(project_facilities, list) and len(project_facilities) > 0:
                facility = project_facilities[0]
                if isinstance(facility, dict):
                    mode = facility.get('mode', 'Online')
            
            cursor.execute('''
                INSERT OR IGNORE INTO projects VALUES (?,?,?,?,?,?,?,?)
            ''', (
                project.get('projectId'),
                station_id,
                project.get('problemBankId'),
                project.get('title'),
                project.get('description'),
                project.get('mentorName'),
                project.get('createdBy'),
                mode
            ))
            
            # Skills
            for skill in project.get('projectSkill', []):
                if not skill:
                    continue
                cursor.execute('''
                    INSERT OR IGNORE INTO project_skills VALUES (?,?)
                ''', (
                    project.get('projectId'),
                    skill.get('skillId')
                ))
            
            # Facilities
            for facility in project.get('projectFacility', []):
                if not facility:
                    continue
                cursor.execute('''
                    INSERT OR IGNORE INTO project_facilities VALUES (?,?,?,?,?)
                ''', (
                    facility.get('projectFacilityId'),
                    project.get('projectId'),
                    facility.get('ugstipend', 0.0),
                    facility.get('currency'),
                    f"{facility.get('officeStartTime', '')}-{facility.get('officeEndTime', '')}"
                ))
    
    conn.commit()

if __name__ == "__main__":
    conn = create_db()
    import_data(conn)
    print("Database created: station_data.db")
>>>>>>> bf2110df8bb1623be4b7b45140e00ae579b78634
    conn.close()    