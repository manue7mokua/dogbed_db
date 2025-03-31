import os 
from .interface import DBDB

def connect(dbname):
    """
    Connect to a database file.
    If the file doesn't exist, it will be created

    Args:
        dbname: The database filename

    Returns:
        An instance of DBDB
    """
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')

    return DBDB(f)