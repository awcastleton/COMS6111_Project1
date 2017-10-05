#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import operator
import requests
import re

from string import Template
from sklearn.feature_extraction.text import TfidfVectorizer

# TODO: query transcript files
# TODO: have it reorder the query words on requery

# Configuration variables
CLIENT_KEY = "AIzaSyCATX_cG2DgsJjFtCdgcThfR2xaH7MSMl0"
ENGINE_KEY = "010829534362544137563:ndji7c0ivva"
PRECISION = 1.0
QUERY = "per se"
OUTPUT_TO_FILE = False
TRANSCRIPT = 'transcript.txt'

# Google API query template
URL = Template("https://www.googleapis.com/customsearch/v1?key=$client_key&cx=$engine_key&q=$query")

# List of json objects based on manually determined relevance
NO_DOCS = []
YES_DOCS = []

def log(s):
    print(s)
    if OUTPUT_TO_FILE:
        with open(TRANSCRIPT,"a") as t:
            t.write(s + "\n")

def print_parameters():
    log("Parameters:")
    log("Client key = " + CLIENT_KEY)
    log("Engine key = " + ENGINE_KEY)
    log("Query      = " + QUERY)
    log("Precision  = %.1f" % (PRECISION))

def print_results_header():
    log("Google Search Results:")
    log("======================")

def print_result(item):
    log("[")
    log(" URL: " + item["link"])
    log(" Title: " + item["title"])
    log(" Summary: " + item["snippet"])
    log("]")

def requery():
    global QUERY
    QUERY = ' '.join(select_new_query())
    query()

def query():
    """Send request to Google Custom Search endpoint."""
    url = URL.substitute(client_key = CLIENT_KEY, engine_key = ENGINE_KEY, query = QUERY)
    log("---")
    log(url)
    log("---")
    response = requests.get(url)
    items = response.json()["items"]
    if len(items) >= 10:
        check_relevance(items)
    else:
        log("Not enough search results!")
        log("%s results returned" % len(items))

def check_relevance(items):
    """Loop through results and ask for manual feedback."""
    print_results_header()
    relevance_counter = 0
    for index in range(len(items)):
        log("Result %d" % (index + 1))
        print_result(items[index])
        relevance = raw_input("Relevant (Y/N)?")

        if relevance.lower() == "y":
            relevance_counter += 1
            YES_DOCS.append(items[index])
        else:
            NO_DOCS.append(items[index])

    print("Precision = %.1f" % (calc_precision(relevance_counter)))
    if relevance_counter > 0 and PRECISION > calc_precision(relevance_counter):
        requery()

def calc_precision(rel_documents):
    return rel_documents / float(10)

def get_words(docs):
    """Returns a list of words from the `title` and `snippet` sections, discounting punctuation"""
    words = []
    for doc in docs:
        words.extend(re.sub("[^\w]", " ", doc["title"]).split())
        words.extend(re.sub("[^\w]", " ", doc["snippet"]).split())
    return words

def tfidf(docs):
    """Return a dict of word: value pairs"""
    words = get_words(docs)
    vectorizer = TfidfVectorizer(stop_words=read_stopwords())
    x = vectorizer.fit_transform(words)
    idf = vectorizer.idf_
    return dict(zip(vectorizer.get_feature_names(), idf))

def ordered_tfidf_diff(yes, no):
    """Returns a sorted list of words that appear in the yes vector only"""
    unique_words = {}
    for key in yes:
        if key not in no:
            unique_words[key] = yes[key]
    return sorted(unique_words.items(), key=operator.itemgetter(1))

def read_stopwords():
    """Returns list of stopwords."""
    f = open("proj1-stop.txt", "r")
    words = f.read().split()
    f.close()
    return words

def select_new_query():
    """Computes the diff between yes and no tfidf vectors and chooses the new query with 2 new words included.  Reorders the words in the query as necessary"""
    no_tfidf = tfidf(NO_DOCS)
    yes_tfidf = tfidf(YES_DOCS)
    diff = ordered_tfidf_diff(yes_tfidf, no_tfidf)

    # Create the new query: The old query plus two new words in descending order of calculated relevance
    new_query = []
    new_words = []
    old_words = QUERY.split()
    for key in diff:
        if key[0] in old_words:
            new_query.append(key[0])
            old_words.remove(key[0])
        elif len(new_words) < 2 and QUERY.find(key[0]) == -1:
            new_query.append(key[0])
            new_words.append(key[0])

    # append any of the old query words that didn't come up in the documents (if any)
    for old_word in old_words:
        new_query.append(old_word)

    return new_query

def main():
    """Main entry point for the script."""
    log('==================================================================')
    
    global CLIENT_KEY
    if len(sys.argv) > 1: CLIENT_KEY = sys.argv[1]

    global ENGINE_KEY
    if len(sys.argv) > 2: ENGINE_KEY = sys.argv[2]

    global PRECISION
    if len(sys.argv) > 3: PRECISION = float(sys.argv[3])

    global QUERY
    if len(sys.argv) > 4: QUERY = sys.argv[4].lower()
    
    global OUTPUT_TO_FILE
    if len(sys.argv) > 5: OUTPUT_TO_FILE = (sys.argv[5].lower() == "true")

    print_parameters()
    query()
    log('==================================================================')

if __name__ == '__main__':
    sys.exit(main())
