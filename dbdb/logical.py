class ValueRef:
    def __init__(self, referent=None, address=0):
        self._referent = referent   # Python object
        self._address = address     # Address on disk

    @property
    def address(self):
        return self._address 

    def get(self, storage):
        # Get the value - from memory if loaded, otherwise from disk
        if self._referent is None and self._address:
            # Value isn't loaded into memory, so fetch it from disk
            data = storage.read(self._address)
            if data:
                # Convert from serialized form to Python object
                self._referent = self.string_to_referent(data)

        return self._referent

    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)

            # Serialize and store
            data = self.referent_to_string(self._referent)
            self._address = storage.write(data)

    def prepare_to_store(self, storage):
        """
        Prepare any dependent objects for storage.
        Should be overriden by subclasses
        """
        pass

    @staticmethod
    def referent_to_string(referent):
        """
        Convert a referent object to a string for storage
        Should be overriden by subclasses
        """
        raise NotImplementedError
    
    @staticmethod
    def string_to_referent(string):
        """
        Convert a string from storage to a referent object
        Should be overriden by subclasses
        """
        raise NotImplementedError
    

class LogicalBase:
    node_ref_class = None   # Subclasses must set this to a ValueRef subclass
    value_ref_class = ValueRef 

    def __init__(self, storage):
        self._storage = storage
        self._refresh_tree_ref()

    def _refresh_tree_ref(self):
        # Refresh the reference to the tree's root node
        self._tree_ref = self.node_ref_class(address=self._storage.get_root_address())

    def commit(self):
        # Save the tree if it has changed
        self._tree_ref.store(self._storage)

        # Update the root address on disk
        self._storage.commit_root_address(self._tree_ref.address)


    def _follow(self, ref):
        return ref.get(self._storage)

    def get(self, key):
        if not self._storage.locked:
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref), key)

    def set(self, key, value):
        if self._storage.lock():
            self._refresh_tree_ref()

        # Create a new tree with the key-value pair inserted
        self._tree_ref = self._insert(
            self._follow(self._tree_ref),
            key,
            self.value_ref_class(value)
        )

    def delete(self, key):
        if self._storage.lock():
            self._refresh_tree_ref()
        
        # Create a new tree with the key deleted
        self._tree_ref = self._delete(
            self._follow(self._tree_ref),
            key
        )

    def _get(self, node, key):
        """
        Get the value for a key in a subtree.
        Subclasses must implement this method.
        """
        raise NotImplementedError

    def _insert(self, node, key, value_ref):
        """
        Insert a key-value pair into a subtree
        Subclasses must implement this method.
        """
        raise NotImplementedError

    def _delete(self, node, key):
        """
        Delete a key from a subtree
        Subclasses must implement this method.
        """
        raise NotImplementedError