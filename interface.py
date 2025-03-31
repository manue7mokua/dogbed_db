from .binary_tree import BinaryTree
from .physical import Storage

class DBDB:
    """
    This class implements the Python dictionary API using BinaryTree
    for storage and retrieval
    """

    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        """Close the database file"""
        self.__storage.close()

    def commit(self):
        """Commit changes to disk"""
        self._assert_not_closed()
        self._tree.commit()

    def __getitem__(self, key):
        """Get a value by key, like dict[key]"""
        self._assert_not_closed()
        return self._tree.get(key)

    def __setitem__(self, key, value):
        """Set a value by key, like dict[key] = value"""
        self._assert_not_closed()
        return self._tree.set(key, value)

    def __delitem__(self, key):
        """Delete a key-value pair, like del dict[key]"""
        self._assert_not_closed()
        return self._tree.delete(key) 

    def __contains__(self, key):
        """Check if key exists, like key in dict"""
        try:
            self[key]
            return True
        except KeyError:
            return False