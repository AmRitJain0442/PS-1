<<<<<<< HEAD
import sqlite3
import sys

def print_table(cursor, rows, headers=None):
    if not rows:
        print("No results found.")
        return
        
    if headers:
        print(" | ".join(headers))
        print("-" * (sum(len(h) for h in headers) + 3 * (len(headers) - 1)))
    
    for row in rows:
        print(" | ".join(str(item) if item is not None else "NULL" for item in row))

def main():
    conn = sqlite3.connect('station_data.db')
    cursor = conn.cursor()
    
    # Enable column names in results
    conn.row_factory = sqlite3.Row
    
    while True:
        print("\nAvailable commands:")
        print("1. List tables")
        print("2. Show table schema")
        print("3. Run custom query")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("\nAvailable tables:")
            for table in tables:
                print(f"- {table[0]}")
                
        elif choice == "2":
            table_name = input("Enter table name: ")
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            schema = cursor.fetchone()
            if schema:
                print(f"\nSchema for {table_name}:")
                print(schema[0])
            else:
                print(f"Table '{table_name}' not found.")
                
        elif choice == "3":
            query = input("Enter your SQL query: ")
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                if cursor.description:
                    headers = [description[0] for description in cursor.description]
                    print_table(cursor, rows, headers)
                else:
                    print("Query executed successfully.")
            except sqlite3.Error as e:
                print(f"Error executing query: {e}")
                
        elif choice == "4":
            break
            
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()

if __name__ == "__main__":
=======
import sqlite3
import sys

def print_table(cursor, rows, headers=None):
    if not rows:
        print("No results found.")
        return
        
    if headers:
        print(" | ".join(headers))
        print("-" * (sum(len(h) for h in headers) + 3 * (len(headers) - 1)))
    
    for row in rows:
        print(" | ".join(str(item) if item is not None else "NULL" for item in row))

def main():
    conn = sqlite3.connect('station_data.db')
    cursor = conn.cursor()
    
    # Enable column names in results
    conn.row_factory = sqlite3.Row
    
    while True:
        print("\nAvailable commands:")
        print("1. List tables")
        print("2. Show table schema")
        print("3. Run custom query")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("\nAvailable tables:")
            for table in tables:
                print(f"- {table[0]}")
                
        elif choice == "2":
            table_name = input("Enter table name: ")
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            schema = cursor.fetchone()
            if schema:
                print(f"\nSchema for {table_name}:")
                print(schema[0])
            else:
                print(f"Table '{table_name}' not found.")
                
        elif choice == "3":
            query = input("Enter your SQL query: ")
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                if cursor.description:
                    headers = [description[0] for description in cursor.description]
                    print_table(cursor, rows, headers)
                else:
                    print("Query executed successfully.")
            except sqlite3.Error as e:
                print(f"Error executing query: {e}")
                
        elif choice == "4":
            break
            
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()

if __name__ == "__main__":
>>>>>>> bf2110df8bb1623be4b7b45140e00ae579b78634
    main() 