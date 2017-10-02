# COMS6111_Project1

Information retrieval with user-provided relevance feedback

## Connecting to the Virtual Machine

External IP: 35.185.22.146 <br/>
user: project1 <br/>
password: passw0rd

sample linux/mac command for connecting to the VM:<br/>
    ssh project1@35.185.22.146<br/>
    passw0rd<br/>

## Running the code

cd COMS6111_Project1 <br/>
sh search.sh /<TARGET PRECISION/> '/<QUERY TERMS/>'

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
* Since the returned snippets and titles of our documents contain a relatively small number of words, we are simply using words that are contained in the relevant documents while NOT being contained in the irrelevant documents.
* We then append to our query the top two words that are left ordered by TF-IDF value.

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
