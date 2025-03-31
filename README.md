# Dogbed_DB - A Simple Key-Value Database

Dogbed_DB is a lightweight, file-based key-value database implementation in Python. It provides a simple dictionary-like interface for storing and retrieving data, with persistence across sessions.

## Features

- Simple dictionary-like interface
- Persistent storage
- Binary tree-based indexing
- Transaction support (commit/rollback)
- Thread-safe operations
- Support for string values

## Project Structure

```
dbdb/
├── __init__.py      # Main interface and connect function
├── interface.py     # Dictionary-like interface implementation
├── logical.py       # Logical layer with value references
├── binary_tree.py   # Binary tree data structure
├── physical.py      # Low-level storage operations
└── tool.py         # Command-line interface
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/manue7mokua/dogbed_db.git
cd dogbed_db
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
import dbdb

# Connect to a database (creates if it doesn't exist)
db = dbdb.connect("my_database.db")

# Store values
db['name'] = 'DBDB'
db['type'] = 'key-value store'

# Commit changes
db.commit()

# Retrieve values
print(db['name'])  # Output: DBDB

# Delete values
del db['type']

# Check if key exists
if 'name' in db:
    print("Key exists!")

# Close the database
db.close()
```

### Command Line Tool

The project includes a command-line tool for basic database operations:

```bash
python -m dbdb.tool my_database.db get key
python -m dbdb.tool my_database.db set key value
python -m dbdb.tool my_database.db delete key
```

## Testing

Run the test suite:

```bash
python -m unittest test_dbdb.py -v
```

Run the manual test script:

```bash
python manual_test.py
```

## Implementation Details

DBDB uses a binary tree data structure for indexing and stores data in a single file. The implementation is divided into several layers:

1. **Physical Layer** (`physical.py`): Handles low-level file operations and storage management.
2. **Logical Layer** (`logical.py`): Implements the logical structure with value references.
3. **Binary Tree** (`binary_tree.py`): Provides the indexing structure for efficient key lookups.
4. **Interface** (`interface.py`): Exposes a dictionary-like API to users.

## Future Improvements

While this implementation works, there are several limitations and potential improvements:

1. **No Garbage Collection**: Old data is never reclaimed, so the database file will keep growing even if you delete keys. A compaction feature will be added.

2. **Limited Concurrency**: The locking mechanism is simple and doesn't allow for concurrent updates. A more sophisticated locking scheme will be implemented to improve performance.

3. **Inefficient For Large Values**: All values are stored as separate records, which is inefficient for large values.

4. **No Indexes**: For more complex data, additional index structures could be useful. Feel free to implement this.

5. **Single File**: The database is stored in a single file, which could be a bottleneck for large databases. A multi-file approach might be better.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

This project is inspired by the need for a simple, file-based key-value store in Python. It's designed to be educational and demonstrate basic database concepts.

The implementation is based on the excellent article "DBDB: Dog Bed Database" by Taavi Burns in the [500 Lines or Less](https://aosabook.org/en/500L/dbdb-dog-bed-database.html) blog, which provides a detailed explanation of building a simple key-value database with proper separation of concerns and immutable data structures.
