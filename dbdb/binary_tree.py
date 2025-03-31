import pickle 
from .logical import LogicalBase, ValueRef

class StringValueRef(ValueRef):
    """Reference to a string value on disk"""
    
    @staticmethod
    def referent_to_string(referent):
        """Serialize a string value to a string"""
        return pickle.dumps(referent)
    
    @staticmethod
    def string_to_referent(string):
        """Deserialize a string value from a string"""
        return pickle.loads(string)

class BinaryNode:
    def __init__(self, left_ref, key, value_ref, right_ref, length):
        self.left_ref = left_ref
        self.key = key 
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.length = length 

    @classmethod
    def from_node(cls, node, **kwargs):
        """Create a new node from an existing one, with some values changed"""
        length = node.length

        if 'left_ref' in kwargs:
            left_ref = kwargs['left_ref']
            length += left_ref.length - node.left_ref.length
        else:
            left_ref = node.left_ref

        if 'right_ref' in kwargs:
            right_ref = kwargs['right_ref']
            length += right_ref.length - node.right_ref.length
        else:
            right_ref = node.right_ref

        return cls(
            left_ref=left_ref,
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=right_ref,
            length=length
        )

    def store_refs(self, storage):
        # Store all references in this node to disk
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)

class BinaryNodeRef(ValueRef):
    """Reference to a binary node on disk"""

    @classmethod
    def length_ref(cls):
        return cls(BinaryNode(
            left_ref=ValueRef(),
            key=None,
            value_ref=ValueRef(),
            right_ref=ValueRef(),
            length=0
        ))

    def prepare_to_store(self, storage):
        # Recursively prepare all refs in this node for storage
        if self._referent:
            self._referent.store_refs(storage)

    @property
    def length(self):
        """Get the number of key-value pairs in this subtree"""
        if self._referent is None and self._address:
            raise RuntimeError("Length unknown for unloaded node")
        if self._referent:
            return self._referent.length
        else:
            return 0

    @staticmethod 
    def referent_to_string(referent):
        """Serialize a BinaryNode to a string"""
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'length': referent.length
        })
    
    @staticmethod
    def string_to_referent(string):
        """Deserialize a BinaryNode from a string"""
        data = pickle.loads(string)

        return BinaryNode(
            left_ref=BinaryNodeRef(address=data['left']),
            key=data['key'],
            value_ref=StringValueRef(address=data['value']),
            right_ref=BinaryNodeRef(address=data['right']),
            length=data['length']
        )

class BinaryTree(LogicalBase):
    """
    A binary tree implementation with immutable nodes.

    When changes are made, new nodes are created with references to unchanged
    parts of the tree
    """
    node_ref_class = BinaryNodeRef
    value_ref_class = StringValueRef  # Use StringValueRef for values

    def _get(self, node, key):
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif node.key < key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
            
        raise KeyError(key)

    def _insert(self, node, key, value_ref):
        # Create a new tree with the key inserted
        if node is None:
            # Empty tree, create a leaf node
            new_node = BinaryNode(
                left_ref=self.node_ref_class(),  # empty left ref
                key=key,
                value_ref=value_ref,
                right_ref=self.node_ref_class(),  # empty right ref
                length=1  # length is 1
            ) 
        elif key < node.key:
            # Key belongs in left subtree
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._insert(
                    self._follow(node.left_ref), key, value_ref
                )
            )
        elif node.key < key:
            # Key belongs in right subtree
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(
                    self._follow(node.right_ref), key, value_ref
                )
            )
        else:
            # Key already exists, update value
            new_node = BinaryNode.from_node(
                node,
                value_ref=value_ref
            )

        return self.node_ref_class(referent=new_node)

    def _delete(self, node, key):
        if node is None:
            raise KeyError(key)
        
        if key < node.key:
            # Key should be in left subtree
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._delete(
                    self._follow(node.left_ref), key
                )
            )
        elif node.key < key:
            # Key should be in right subtree
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._delete(
                    self._follow(node.right_ref), key 
                )
            )
        else:
            # Found the key, now handle deletion
            left = self._follow(node.left_ref)
            right = self._follow(node.right_ref)

            if left is None and right is None:
                # This is a leaf node, just delete it
                return self.node_ref_class()
            elif left is None:
                # Only right child, replace with right
                return node.right_ref
            elif right is None:
                # Only left child, replace with left
                return node.left_ref
            else:
                # Two children - find the successor (smallest key in right subtree)
                successor = self._find_min(right)

                # Create a new node with the successor as the key
                new_node = BinaryNode.from_node(
                    node,
                    key=successor.key,
                    value_ref=successor.value_ref,
                    right_ref=self._delete(
                        right, successor.key
                    )
                )

        return self.node_ref_class(referent=new_node)

    def _find_min(self, node):
        """Find the node with the minimum key in a subtree"""
        while self._follow(node.left_ref) is not None:
            node = self._follow(node.left_ref)
        return node 