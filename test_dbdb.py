import os
import tempfile
import unittest
import dbdb

class TestDBDB(unittest.TestCase):
    """Tests for the DBDB class"""

    def setUp(self):
        """Create a temporary database file for testing"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.db = dbdb.connect(self.temp_file.name)

    def tearDown(self):
        """Close the database and remove the temporary file"""
        self.db.close()
        os.unlink(self.temp_file.name)

    def test_set_get(self):
        """Test setting and getting values"""
        self.db['key1'] = 'value1'
        self.db.commit()
        self.assertEqual(self.db['key1'], 'value1')

        self.db['key2'] = 'value2'
        self.assertEqual(self.db['key2'], 'value2')

        # Reopen database to test persistence
        self.db.close()
        db2 = dbdb.connect(self.temp_file.name)

        self.assertEqual(db2['key1'], 'value1')

        with self.assertRaises(KeyError):
            db2['key2']

        db2.close()

    def test_delete(self):
        """Test deleting values"""
        self.db['key'] = 'value'
        self.db.commit()

        del self.db['key']
        with self.assertRaises(KeyError):
            self.db['key']

        # Deleting does not persist until commit
        self.db.close()
        db2 = dbdb.connect(self.temp_file.name)
        self.assertEqual(db2['key'], 'value')

        del db2['key']
        db2.commit()

        # Reopen to check persistence
        db2.close()
        db3 = dbdb.connect(self.temp_file.name)
        with self.assertRaises(KeyError):
            db3['key']

        db3.close()

    def test_contains(self):
        """Test the 'in' operator"""
        self.db['key'] = 'value'
        self.assertTrue('key' in self.db)
        self.assertFalse('nonexistent' in self.db)

    def test_overwrite(self):
        """Test overwriting values"""
        self.db['key'] = 'value1'
        self.db['key'] = 'value2'
        self.assertEqual(self.db['key'], 'value2')

if __name__ == '__main__':
    unittest.main()