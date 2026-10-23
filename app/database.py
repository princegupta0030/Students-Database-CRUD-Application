import sqlite3

DATABASE_URL = "students.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            course TEXT,
            address TEXT,
            enrollment_date TEXT
        )
    """)

    # Check if the table needs schema updates (for development environment transitions)
    # We will check if 'date_of_birth' exists, if not, we perform a safe schema migration
    cursor.execute("PRAGMA table_info(students)")
    columns = [info['name'] for info in cursor.fetchall()]

    if 'date_of_birth' not in columns:
        # Perform a safe migration by creating a temporary table, copying data, and replacing
        cursor.execute("BEGIN TRANSACTION")

        # Create new table with updated schema
        cursor.execute("""
            CREATE TABLE students_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL DEFAULT '1970-01-01',
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                course TEXT,
                address TEXT,
                enrollment_date TEXT
            )
        """)

        # Copy existing data (using default for date_of_birth since it's required in the new schema)
        # Assuming the old schema had 'age' which we are dropping, and didn't have phone/course/address/enrollment_date
        cursor.execute("""
            INSERT INTO students_new (id, name, email)
            SELECT id, name, email FROM students
        """)

        # Drop the old table and rename the new one
        cursor.execute("DROP TABLE students")
        cursor.execute("ALTER TABLE students_new RENAME TO students")

        cursor.execute("COMMIT")

    conn.commit()
    conn.close()
