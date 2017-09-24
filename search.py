import sys
import requests

from string import Template

CLIENT_KEY = ""
ENGINE_KEY = ""
PRECISION = 1.0
QUERY = ""
_QUERY = "" # placeholder for original query term

URL = Template("https://www.googleapis.com/customsearch/v1?key=$client_key&cx=$engine_key&q=$query")

KEYWORD_MAP = {}

def print_parameters():
    print "Parameters:"
    print "Client key = " + CLIENT_KEY
    print "Engine key = " + ENGINE_KEY
    print "Query      = " + QUERY
    print "Precision  = %.1f" % (PRECISION)

def print_results_header():
    print "Google Search Results:"
    print "======================"

def print_result(item):
    print "["
    print " URL: " + item["link"]
    print " Title: " + item["title"]
    print " Summary: " + item["snippet"]
    print "]"

def requery():
    global QUERY

    # simply pop the top two repeating terms each time
    sorted_keys = sorted(KEYWORD_MAP, key=KEYWORD_MAP.get, reverse=True)

    # TODO - don't repeat the same top keys on subsequent searches
    QUERY = QUERY + " " + sorted_keys[0] + " " + sorted_keys[1]
    query()

def query():
    """Send request to Google Custom Search endpoint."""
    url = URL.substitute(client_key = CLIENT_KEY, engine_key = ENGINE_KEY, query = QUERY)
    print "---"
    print url
    print "---"
    response = requests.get(url)
    items = response.json()["items"]
    check_relevance(items)

def check_relevance(items):
    """Loop through results and ask for manual feedback."""
    print_results_header()
    for index in range(len(items)):
        print "Result %d" % (index + 1)
        print_result(items[index])
        relevance = raw_input("Relevant (Y/N)?")

        if relevance == "Y":
            add_to_keyword_index(items[index])

    requery()

def add_to_keyword_index(item):
    """List of words that appear in the titles of relevant entries."""
    global KEYWORD_MAP

    words = item["title"].split()
    for word in words:
        word = word.lower()
        # TODO - make this a more legitament stop-word filter
        if len(word) > 1 and _QUERY.find(word) == -1:
            if word in KEYWORD_MAP:
                KEYWORD_MAP[word] = KEYWORD_MAP[word]+ 1
            else:
                KEYWORD_MAP[word] = 0

def main():
    """Main entry point for the script."""
    global CLIENT_KEY
    CLIENT_KEY = sys.argv[1]

    global ENGINE_KEY
    ENGINE_KEY = sys.argv[2]

    global PRECISION
    PRECISION = float(sys.argv[3])

    global QUERY, _QUERY
    QUERY = "per se" #sys.argv[4].lower()
    _QUERY = QUERY

    print_parameters()
    query()

if __name__ == '__main__':
    sys.exit(main())
