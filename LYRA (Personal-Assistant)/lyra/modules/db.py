import csv
import sqlite3

con = sqlite3.connect("LYRA.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
cursor.execute(query)
con.commit()

# Add more common Windows applications
query = "INSERT INTO sys_command VALUES (null,'notepad', 'C:\\Windows\\System32\\notepad.exe')"
cursor.execute(query)
con.commit()

query = "INSERT INTO sys_command VALUES (null,'calculator', 'C:\\Windows\\System32\\calc.exe')"
cursor.execute(query)
con.commit()

query = "INSERT INTO sys_command VALUES (null,'paint', 'C:\\Windows\\System32\\mspaint.exe')"
cursor.execute(query)
con.commit()

query = "INSERT INTO sys_command VALUES (null,'wordpad', 'C:\\Windows\\System32\\write.exe')"
cursor.execute(query)
con.commit()

query = "INSERT INTO sys_command VALUES (null,'command prompt', 'C:\\Windows\\System32\\cmd.exe')"
cursor.execute(query)
con.commit()

query = "INSERT INTO sys_command VALUES (null,'file explorer', 'C:\\Windows\\explorer.exe')"
cursor.execute(query)
con.commit()

query = "INSERT INTO sys_command VALUES (null,'task manager', 'C:\\Windows\\System32\\Taskmgr.exe')"
cursor.execute(query)
con.commit()

query = "INSERT INTO sys_command VALUES (null,'control panel', 'C:\\Windows\\System32\\control.exe')"
cursor.execute(query)
con.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
cursor.execute(query)
con.commit()


# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL, address VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 30]

# Read data from CSV and insert into SQLite table for the desired columns
# Uncomment the following code to import from CSV
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     next(csvreader, None)  # Skip header if exists
#     for row in csvreader:
#         if len(row) >= 2:
#             name = row[0].strip()
#             mobile = row[1].strip()
#             email = row[2].strip() if len(row) > 2 else None
#             city = row[3].strip() if len(row) > 3 else None
#             cursor.execute('''INSERT INTO contacts VALUES (null, ?, ?, ?, ?)''', (name, mobile, email, city))

# con.commit()

query = "INSERT INTO contacts VALUES (null,'Deepak', '1234567890', NULL, NULL)"
cursor.execute(query)
con.commit()

# query = 'kunal'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

# Adding personal info table
query = "CREATE TABLE IF NOT EXISTS info(name VARCHAR(100), designation VARCHAR(50),mobileno VARCHAR(40), email VARCHAR(200), city VARCHAR(300))"
cursor.execute(query)

# Add Column in contacts table
# cursor.execute("ALTER TABLE contacts ADD COLUMN address VARCHAR(255)")

