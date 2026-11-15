import sqlite3

conn = sqlite3.connect('instance/sdth.db')

print("--- المستخدمين ---")
users = conn.execute("SELECT id, username, role FROM user").fetchall()
for u in users:
    print(u)

print("--- الشاحنات ---")
trucks = conn.execute("SELECT id, plate_number, qr_code, status FROM truck").fetchall()
for t in trucks:
    print(t)

conn.close()