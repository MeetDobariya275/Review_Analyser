import sqlite3

def create_database():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    # Create the reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_id TEXT NOT NULL,
            author_name TEXT,
            rating REAL,
            review_text TEXT,
            timestamp TEXT,
            sentiment TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database and table created successfully.")

if __name__ == "__main__":
    create_database()
