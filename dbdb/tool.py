import sys
import dbdb

OK = 0
BAD_ARGS = 1
BAD_VERB = 2
BAD_KEY = 3

def usage():
    print("Usage:", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME get KEY", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME set KEY VALUE", file=sys.stderr)
    print("\tpython -m dbdb.tool DBNAME delete KEY", file=sys.stderr)

def main(argv):
    """
    Args:
        argv: Command line arguments

    Returns:
        Exit code
    """
    if not(4 <= len(argv) <=5):
        usage()
        return BAD_ARGS
    
    dbname, verb, key = argv[1:4]
    value = argv[4] if len(argv) == 5 else None 

    if verb not in {'get', 'set', 'delete'}:
        usage()
        return BAD_VERB
    
    db = dbdb.connect(dbname)

    try:
        if verb == 'get':
            sys.stdout.write(db[key])
        elif verb == 'set':
            db[key] = value
            db.commit()
        else:
            del db[key]
            db.commit()
    except KeyError:
        print("Key not found", file=sys.stderr)
        return BAD_KEY
    finally:
        db.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))