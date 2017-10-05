# COMS6111_Project1

Group: Project 1 Group 21

Information retrieval with user-provided relevance feedback

## Files Included in Submission

* search.py - contains all program logic and implementation
* search.sh - an entry point to search.py, provided for convenience (so you dont need to provide the key and engine ID every time)
* transcript.txt - A simple transcript of the printouts provided by search.py, using the test-cases "per se", "brin" and "jaguar"
* proj1-stop.txt - The set of stop words that we used in our program

## Connecting to the Virtual Machine

External IP: 35.185.22.146 <br/>
user: project1 <br/>
password: passw0rd

sample linux/mac command for connecting to the VM:<br/>
    ssh project1@35.185.22.146<br/>
    passw0rd<br/>

## Running the code

NOTE: executes on Python 2.7!

cd COMS6111_Project1 <br/>
sh search.sh &lt;TARGET_PRECISION&gt; '&lt;QUERY TERMS&gt;'

The code will:
* Return results one-at-a-time until 10 results have been shown
* Results will contain the url, the title and a snippet of the contents of the document
* User will be asked a binary question of relevance: (Y/N)
* Once all 10 results have been evaluated by the user as either relevant or irrelevant, it evaluates the precision@10
* If the precision@10 is zero or greater than or equal to the target precision, the program terminates
* Otherwise it re-evaluates the query using the user-provided feedback to create new query terms which get appended to the original query
* This process repeats until either the precision@10 is 0 or greater than or equal to the target precision

## Query Re-Evaluation

* Goal: We want to modify our query to include things that accurately describe the relevant documents without describing the irrelevant ones.
* We compute the TF-IDF scores for the relevant and irrelevant documents separately.
* Since the returned snippets and titles of our documents contain a relatively small number of words, we are simply using words that are contained in the relevant documents while NOT being contained in the irrelevant documents.  This turned out to be significantly more-successful than simply taking the difference of the two sets of scores (which was our original implementation).
* We then re-build the query with our original words and two new words, sorted in descening order of tf-idf value among the relevant documents.  If original words appeared in the non-relevant documents or did not appear in a relevant document, they are simply appended to the end of the query in the order that they were originally provided

## Notes

Custom Search API key:
AIzaSyCATX_cG2DgsJjFtCdgcThfR2xaH7MSMl0

Search Engine ID:
010829534362544137563:ndji7c0ivva

sample exec cmd:
/home/paparrizos/run

Notes:
had to:
pip install sklearn
pip install numpy (requirement of sklearn)
pip install scipy (requirement of sklearn)
