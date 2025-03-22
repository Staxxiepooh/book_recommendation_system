import sqlite3

USER_RATINGS_FILE = 'user_ratings.db'

conn = sqlite3.connect(USER_RATINGS_FILE)
cursor = conn.cursor()
cursor.execute("DELETE FROM ratings")  # Delete all rows
conn.commit()
conn.close()

print("Database cleared successfully!")
