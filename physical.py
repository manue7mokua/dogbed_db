# Handles how data is stored on disk

import os
import struct
import portalocker 

class Storage():
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = '!Q'
    INTEGER_LENGTH = 8

    def __init__(self, f):
        self._f= f
        self.locked = False 
        # Ensures we start with a valid superblock
        self.ensure_superblock()

    def _ensure_superblock(self):
        self.lock()
        self._f.seek(0, os.SEEK_END)
        end_address = self._f.tell()

        if end_address < self.SUPERBLOCK_SIZE:
            # File is empty or too small, create superblock
            self._f.seek(0)
            self._f.write(b'\x00' * self.SUPERBLOCK_SIZE)
        
        self.unlock()
        
    def _seek_superblock(self):
        "Move file cursor to beginning of the superblock"
        self._f.seek(0)
        
    def _seek_end(self):
        "Move cursor to the end of the file"
        self._f.seek(0, os.SEEK_END)

    def _read_integer(self):
        "Read an integer from the current position"
        int_bytes = self._f.read(self.INTEGER_LENGTH)
        return struct.unpack(self.INTEGER_FORMAT, int_bytes)[0]

    def _write_integer(self, integer):
        "Write an integer to the current position"
        self._f.write(struct.pack(self.INTEGER_FORMAT, integer))

    def lock(self):
        "Lock databse file for exclusive access"
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        "Unlock the database file"
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def get_root_address(self):
        "Get the address of the root node"
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def commit_root_address(self, root_address):
        "Save the root address to disk"
        self.lock()
        self._f.flush()
        self._seek_superblock()
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def write(self, data):
        "Write data to disk and return its address"
        self.lock()
        self._seek_end()
        object_address = self._f.tell()

        # Write data length followed by the data itself
        self._write_integer(len(data))
        self._f.write(data)

        return object_address
    
    def read(self, address):
        "Read data from give address"
        if address == 0:
            return None
        
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data
    
    @property
    def closed(self):
        "Check if the file is closed"
        return self._f.closed

    def close(self):
        "Close the file"
        self.unlock()
        self._f.close()
