import sqlite3

def create_database():
    connection = sqlite3.connect("blood_system.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blood_group TEXT NOT NULL,
            contact_number TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blood_group TEXT NOT NULL,
            required_units INTEGER NOT NULL,
            hospital_name TEXT NOT NULL,
            contact_number TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

create_database()

print("Database created successfully!")