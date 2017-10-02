#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import operator
import requests

from string import Template
from sklearn.feature_extraction.text import TfidfVectorizer

# Configuration variables
CLIENT_KEY = "AIzaSyCATX_cG2DgsJjFtCdgcThfR2xaH7MSMl0"
ENGINE_KEY = "010829534362544137563:ndji7c0ivva"
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
    global QUERY
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
    relevance_counter = 0
    for index in range(len(items)):
        print("Result %d" % (index + 1))
        print_result(items[index])
        relevance = raw_input("Relevant (Y/N)?")

        if relevance.lower() == "y":
            relevance_counter += 1
            YES_DOCS.append(items[index])
        else:
            NO_DOCS.append(items[index])

    print "Precision = %.1f" % (calc_precision(relevance_counter))
    if relevance_counter > 0 and PRECISION > calc_precision(relevance_counter):
        requery()

def calc_precision(rel_documents):
    return rel_documents / float(10)

def get_words(docs):
    """Returns a list of words from the `title` and `snippet` sections"""
    words = []
    for doc in docs:
        words.extend(doc["title"].split())
        words.extend(doc["snippet"].split())
    return words

def tfidf(docs):
    """Return a dict of word: value pairs"""
    words = get_words(docs)
    vectorizer = TfidfVectorizer(stop_words=read_stopwords())
    x = vectorizer.fit_transform(words)
    idf = vectorizer.idf_
    return dict(zip(vectorizer.get_feature_names(), idf))

def ordered_tfidf_diff(yes, no):
    """Removes any words repeated between both yes and no vectors and returns a sorted list of tuples"""
    unique_words = {}
    for key in yes:
        if key not in no:
            unique_words[key] = yes[key]
    return sorted(unique_words.items(), key=operator.itemgetter(1))

def read_stopwords():
    """Returns list of stopwords."""
    f = open("proj1-stop.txt", "r")
    words = f.read().split()
    return words

def select_new_words():
    """Computes the diff between yes and no tfidf vectors and chooses the next words to add to the query"""
    no_tfidf = tfidf(NO_DOCS)
    yes_tfidf = tfidf(YES_DOCS)
    diff = ordered_tfidf_diff(yes_tfidf, no_tfidf)

    new_words = []
    for key in diff:
        if len(new_words) < 2 and QUERY.find(key[0]) == -1:
            new_words.append(key[0])

    return new_words

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
    print("finished")

if __name__ == '__main__':
    sys.exit(main())
