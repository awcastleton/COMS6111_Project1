import sys
import requests

from string import Template

CLIENT_KEY = ""
ENGINE_KEY = ""
PRECISION = 1.0
QUERY = ""

URL = Template("https://www.googleapis.com/customsearch/v1?key=$client_key&cx=$engine_key&q=$query")

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
        items[index]["relevance"] = raw_input("Relevant (Y/N)?")

def main():
    """Main entry point for the script."""
    global CLIENT_KEY
    CLIENT_KEY = sys.argv[1]

    global ENGINE_KEY
    ENGINE_KEY = sys.argv[2]

    global PRECISION
    PRECISION = float(sys.argv[3])

    global QUERY
    QUERY = "per se" #sys.argv[4]

    print_parameters()
    query()

if __name__ == '__main__':
    sys.exit(main())
