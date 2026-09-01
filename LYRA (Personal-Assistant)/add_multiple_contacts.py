# #!/usr/bin/env python3
# """
# Script to add multiple contacts to LYRA database
# """

# import sqlite3
# from engine.features import InsertMultipleContacts, importContactsFromCSV

# def add_contacts_manually():
#     """Add contacts one by one"""
#     print("Adding contacts manually...")

#     # List of contacts as tuples: (name, mobile, email, city)
#     contacts = [
#         ("Rahul Sharma", "9876543210", "rahul@email.com", "Delhi"),
#         ("Priya Singh", "8765432109", "priya@email.com", "Mumbai"),
#         ("Amit Kumar", "7654321098", "amit@email.com", "Bangalore"),
#         ("Sneha Patel", "6543210987", "sneha@email.com", "Ahmedabad"),
#         ("Vikram Joshi", "5432109876", "vikram@email.com", "Pune"),
#         ("Deepak Maurya", "6307034909", "deepak.ukathi@gmail.com", "Varanasi")
#     ]

#     result = InsertMultipleContacts(contacts)
#     print(result)

# def add_contacts_from_csv():
#     """Add contacts from CSV file"""
#     print("Adding contacts from CSV...")
#     result = importContactsFromCSV('contacts_sample.csv')
#     print(result)

# def add_contacts_sqlite_direct():
#     """Add contacts directly using SQLite"""
#     print("Adding contacts directly to database...")

#     con = sqlite3.connect("LYRA.db")
#     cursor = con.cursor()

#     contacts = [
#         ("Ravi Verma", "9876543211", "ravi@email.com", "Chennai"),
#         ("Kavita Rao", "8765432110", "kavita@email.com", "Hyderabad"),
#         ("Suresh Reddy", "7654321110", "suresh@email.com", "Kolkata"),
#         ("Deepak Maurya", "6307034909", "deepak.ukathi@gmail.com", "Varanasi")
#         ("Aditya","+919839940491","Gazipur")
#     ]

#     try:
#         cursor.executemany(
#             '''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''',
#             [(None, name, mobile, email, city) for name, mobile, email, city in contacts]
#         )
#         con.commit()
#         print(f"Successfully added {len(contacts)} contacts directly")
#     except Exception as e:
#         con.rollback()
#         print(f"Error: {e}")
#     finally:
#         con.close()

# def view_all_contacts():
#     """View all contacts in database"""
#     print("\nCurrent contacts in database:")
#     con = sqlite3.connect("LYRA.db")
#     cursor = con.cursor()
#     cursor.execute("SELECT id, name, mobile_no, email, city FROM contacts")
#     contacts = cursor.fetchall()
#     con.close()

#     if contacts:
#         print(f"Total contacts: {len(contacts)}")
#         for contact in contacts:
#             print(f"ID: {contact[0]}, Name: {contact[1]}, Mobile: {contact[2]}, Email: {contact[3] or 'N/A'}, City: {contact[4] or 'N/A'}")
#     else:
#         print("No contacts found")

# if __name__ == "__main__":
#     print("Multiple Contacts Addition Demo")
#     print("=" * 40)

#     # Uncomment the methods you want to test
#     # add_contacts_manually()
#     # add_contacts_from_csv()
#     # add_contacts_sqlite_direct()

#     view_all_contacts()