import sqlite3

conn = sqlite3.connect('smartbursary.db')
cur = conn.cursor()
cur.execute('ALTER TABLE bursaries ADD COLUMN constituency VARCHAR(100) DEFAULT ""')
conn.commit()
conn.close()
print('✓ Added constituency column to database')