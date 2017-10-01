import os
import sys
import requests

from string import Template
# from sklearn.feature_extraction.text import TfidfVectorizer

# Configuration variables
CLIENT_KEY = "AIzaSyCATX_cG2DgsJjFtCdgcThfR2xaH7MSMl0"
ENGINE_KEY = "010829534362544137562:ndji7c0ivva"
PRECISION = 1.0
QUERY = "per se"

# Google API query template
URL = Template("https://www.googleapis.com/customsearch/v1?key=$client_key&cx=$engine_key&q=$query")

# List of json objects based on manually determined relevance
NO_DOCS = []
YES_DOCS = []

def print_parameters():
    print("Parameters:")
    print("Client key = " + CLIENT_KEY)
    print("Engine key = " + ENGINE_KEY)
    print("Query      = " + QUERY)
    print("Precision  = %.1f" % (PRECISION))

def print_results_header():
    print("Google Search Results:")
    print("======================")

def print_result(item):
    print("[")
    print(" URL: " + item["link"])
    print(" Title: " + item["title"])
    print(" Summary: " + item["snippet"])
    print("]")

def requery():
    for word in select_new_words():
        QUERY += ' ' + word
    query()

def query():
    """Send request to Google Custom Search endpoint."""
    url = URL.substitute(client_key = CLIENT_KEY, engine_key = ENGINE_KEY, query = QUERY)
    print("---")
    print(url)
    print("---")
    response = requests.get(url)
    items = response.json()["items"]
    check_relevance(items)

def check_relevance(items):
    """Loop through results and ask for manual feedback."""
    print_results_header()
    for index in range(len(items)):
        print("Result %d" % (index + 1))
        print_result(items[index])
        relevance = raw_input("Relevant (Y/N)?")

        if relevance.lower() == "y":
            YES_DOCS.append(items[index])
        else:
            NO_DOCS.append(items[index])

    print "Precision = %.1f" % (calc_precision())
    # if PRECISION > calc_precision():
    #     requery()

def calc_precision():
    return len(YES_DOCS) / float(10)

def tfidf(docs):
    #TODO - return a dict of word: value pairs
    pass

def tfidf_diff(yes, no):
    #TODO - returns ordered list of yes-no words
    pass

def read_stopwords():
    """Returns list of stopwords."""
    f = open("proj1-stop.txt", "r")
    words = f.read().split()
    return words

def select_new_words():
    #TODO - selects top two (maybe more smart later ; min threshold?) that isn't in stopwords set and not already in query
    # calls tfidf and tfidf_diff and read_stopwords
    pass

def main():
    """Main entry point for the script."""
    global CLIENT_KEY
    if len(sys.argv) > 1: CLIENT_KEY = sys.argv[1]

    global ENGINE_KEY
    if len(sys.argv) > 2: ENGINE_KEY = sys.argv[2]

    global PRECISION
    if len(sys.argv) > 3: PRECISION = float(sys.argv[3])

    global QUERY
    if len(sys.argv) > 4: QUERY = sys.argv[4].lower()

    print_parameters()
    query()

if __name__ == '__main__':
    sys.exit(main())
