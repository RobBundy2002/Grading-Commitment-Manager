import sqlite3

conn = sqlite3.connect('grading_commitments.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS commitments (
        user TEXT,
        subject TEXT,
        PRIMARY KEY (user, subject)
    )
''')
conn.commit()