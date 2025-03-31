"""Demonstrates how to use DBDB in a Python program"""

import os
import dbdb

def main():
    # Delete the database file if it exists
    if os.path.exists("test.db"):
        os.unlink("test.db")

    print("Create database...")
    db = dbdb.connect("test.db")

    print("Setting values...")
    db['name'] = 'DBDB'
    db['type'] = 'key-value store'
    db['creator'] = 'you'

    print("Committing changes...")
    db.commit()

    # Get values
    print("\nStored values:")
    print(f"name: {db['name']}")
    print(f"type: {db['type']}")
    print(f"creator: {db['creator']}")

    # Update a value
    print("\nUpdating a value...")
    db['creator'] = 'Iman Mokua'
    db.commit()

    # Close the database
    db.close()

    # Reopen the database to show persistence
    print("\nReopening database...")
    db2 = dbdb.connect("test.db")

    # Check the updated value
    print(f"creator: {db2['creator']}")

    # Delete a key
    print("\nDeleting a key...")
    del db2['type']
    db2.commit()

    # Check if the key exists
    print(f"'name' in db: {'name' in db2}")
    print(f"'type' in db: {'type' in db2}")

    # Close the database
    db2.close()

    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()
