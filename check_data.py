<<<<<<< HEAD
import json

with open('data.json') as f:
    data = json.load(f)

# Get the first station's data
first_station = next(iter(data['data'].values()))
print("First station keys:", first_station.keys())

# Get the first project's data
if 'project_details' in first_station:
    first_project = next(iter(first_station['project_details'].values()))
    print("\nFirst project keys:", first_project.keys())
    print("\nFirst project mode:", first_project.get('mode'))
=======
import json

with open('data.json') as f:
    data = json.load(f)

# Get the first station's data
first_station = next(iter(data['data'].values()))
print("First station keys:", first_station.keys())

# Get the first project's data
if 'project_details' in first_station:
    first_project = next(iter(first_station['project_details'].values()))
    print("\nFirst project keys:", first_project.keys())
    print("\nFirst project mode:", first_project.get('mode'))
>>>>>>> bf2110df8bb1623be4b7b45140e00ae579b78634
    print("\nFirst project data:", json.dumps(first_project, indent=2)) 