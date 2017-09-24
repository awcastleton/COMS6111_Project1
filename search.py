import sys

CLIENT_KEY = ""
ENGINE_KEY = ""
PRECISION = 1.0
QUERY = ""

def print_parameters():
    print "Parameters:"
    print "Client key = " + CLIENT_KEY
    print "Engine key = " + ENGINE_KEY
    print "Query      = " + QUERY
    print "Precision  = %.1f" % (PRECISION)


def main():
    """Main entry point for the script."""
    global CLIENT_KEY
    CLIENT_KEY = sys.argv[1]

    global ENGINE_KEY
    ENGINE_KEY = sys.argv[2]

    global PRECISION
    PRECISION = float(sys.argv[3])

    global QUERY
    QUERY = sys.argv[4]

    print_parameters()

if __name__ == '__main__':
    sys.exit(main())
