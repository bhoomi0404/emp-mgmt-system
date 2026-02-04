from app.db.connection import get_conn
conn = get_conn()
cur = conn.cursor()
cur.execute("SHOW TABLES LIKE 'employees'")
print(cur.fetchall())
conn.close()
