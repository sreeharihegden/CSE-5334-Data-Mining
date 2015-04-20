#####begin put all your imports 
import nltk
import pymongo
from pymongo import MongoClient

from bs4 import BeautifulSoup
from collections import defaultdict, Counter

#####end put all your imports 


mongodb_client = None
mongodb_db = None
document_frequency = defaultdict(int)
total_number_of_docs = 0


def setup_mongodb():
    #####################Task t2a: your code #######################
    # Connect to mongodb
    mongodb_client = MongoClient()
    mongodb_db = mongodb_client['uta-edu-corpus']
    #####################Task t2a: your code #######################


# This function processes the entire document corpus
def process_document_corpus(file_name):
    #####################Task t2b: your code #######################
    #### The input is a file where in each line you have two information
    #   filename and url separated by |
    # Process the file line by line
    #   and for each line call the function process_document with file name and url and index
    #   first file should have an index of 0, second has 1 and so on
    #Remember to set total_number_of_docs to number of documents
    #####################Task t2b: your code #######################

    with open(file_name) as doc_corpus:
        index = 0
        for line in doc_corpus:
            process_document(line.split('|')[0], line.split('|')[1], index)
            index += 1


#This function processes a single web page and inserts it into mongodb
def process_document(file_name, url, index):
    #Do not change 
    f = open(file_name)
    file_contents = f.read()
    f.close()

    soup = BeautifulSoup(file_contents)


    #####################Task t2c: your code #######################
    #Using the functions that you will write (below), convert the document
    #   into the following structure:
    # title_processed: a string that contains the title of the string after processing
    # hx_processed: an array of strings where each element is a processed string
    #   for eg, if the document has two h1 tags, then the array h1_processed will have two elements
    #   one for each h1 tag and contains its contentent after processing
    # a_processed: same for a tags
    # body_processed: a string that contains body of the document after processing

    title_processed = soup.title.string
    h1_processed = [str(header.text) for header in soup.find_all('h1')]
    h2_processed = [str(header.text) for header in soup.find_all('h2')]
    h3_processed = [str(header.text) for header in soup.find_all('h3')]
    h4_processed = [str(header.text) for header in soup.find_all('h4')]
    h5_processed = [str(header.text) for header in soup.find_all('h5')]
    h6_processed = [str(header.text) for header in soup.find_all('h6')]
    a_processed = [str(link.href) for link in soup.SoupStrainer('a')]
    body_processed = None

    #Insert the processed document into mongodb
    #Do not change 
    webpages = mongodb_db.webpages
    document_to_insert = {
        "url": url,
        "title": title_processed,
        "h1": h1_processed,
        "h2": h2_processed,
        "h3": h3_processed,
        "h4": h4_processed,
        "h5": h5_processed,
        "h6": h6_processed,
        "a": a_processed,
        "body": body_processed,
        "filename": file_name,
        "index": index
    }
    webpage_id = webpages.insert_one(document_to_insert)
    #####################Task t2c: your code #######################

    #Do not change below
    #Write the processed document
    new_file_name = file_name.replace("downloads/", "processed/")
    f = open("processedFileNamesToUUID.txt", "a")
    f.write(new_file_name + "|" + url + "\n")
    f.flush()
    f.close()

    f = open(new_file_name, "w")
    f.write(body_processed)
    f.close()


#helper function for h tags and a tags
# use if needed
def process_array(array):
    processed_array = [process_text(element) for element in array]
    return processed_array


#This function does the necessary text processing of the text
def process_text(text):
    processed_text = ""

    #####################Task t2d: your code #######################
    #Given the text, do the following:
    #   convert it to lower case
    #   remove all stop words (English)
    #   remove all punctuation 
    #   stem them using Porter Stemmer
    #   Lemmatize it
    #####################Task t2d: your code #######################

    return processed_text


#This function determines the vocabulary after processing
def find_corpus_vocabulary(file_name):
    vocabulary = None
    top_5000_words = None
    #Document frequency is a dictionary
    #   given a word, it will tell you how many documents this word was present it
    # use the variable document_frequency 
    document_frequency = defaultdict(int)
    #####################Task t2e: your code #######################
    # The input is the file name with url and processed file names
    # for each file:
    #   get all the words and compute its frequency (over the entire corpus)
    # return the 5000 words with highest frequency
    # Hint: check out Counter class in Python
    #####################Task t2e: your code #######################

    f = open("vocabulary.txt", "w")
    for word in top_5000_words:
        f.write(word + "," + document_frequency[word] + "\n")
    f.close()

    return top_5000_words


def corpus_to_document_vec(vocabulary_file_name, file_name, output_file_name):
    #####################Task t2f: your code #######################
    # The input is the file names of vocabulary, and 
    #   the file  with url, processed file names  and the output file name
    #   the output is a file with tf-idf vector for each document
    #Pseudocode:
    # for each file:
    #   call the function text_to_vec with document body
    #   write the vector into output_file_name one line at a time
    #   into output_file_name
    #       ie document i will be in the i-th line
    #####################Task t2f: your code #######################
    pass


def text_to_vec(vocabulary, text):
    #####################Task t2g: your code #######################
    # The input are vocabulary and text
    #   compute its tf-idf vector (ignore all words not in vocabulary)
    #Remember to use the variable document_frequency for computing idf
    #####################Task t2g: your code #######################
    pass


def query_document_similarity(query_vec, document_vec):
    #####################Task t2h: your code #######################
    #   Given a query and document vector
    #   compute their cosine similarity
    cosine_similarity = None
    #####################Task t2h: your code #######################
    return cosine_similarity


def rank_documents_tf_idf(query, k=10):
    #####################Task t2i: your code #######################

    #convert query to document using text_to_vec function
    query_as_document = None
    ranked_documents = None
    #Write code for the following:
    #   transform the query using process_text
    #   issue the transformed query to mongodb
    #   get ALL matching documents
    #   for each matching document:
    #       retrieve its tf-idf vector (use the file_name and index fields from mongodb)
    #   compute the tf-idf score and sort them accordingly 
    # return top-k documents
    #####################Task t2i: your code #######################
    return ranked_documents[:k]


def rank_documents_zone_scoring(query, k=10):
    #####################Task t2j: your code #######################

    #convert query to document using text_to_vec function
    query_as_document = None
    ranked_documents = None
    #Write code for the following:
    #   transform the query using process_text
    #   issue the transformed query to mongodb
    #   get ALL matching documents
    #   for each matching document compute its score as following:
    #       score = 0
    #       for each word in query:
    #           find which "zone" the word fell in and give appropriate score
    #           title = 0.3, h1 = 0.2, h2=0.1, h3=h4=h5=h6=0.05,a: 0.1, body: 0.1
    #   so if a query keyword occured in title, h1 and body, its score is 0.6
    #       compute this score for all keywords
    #       score of the document is the score of all keywords
    # return top-k documents
    #####################Task t2j: your code #######################
    return ranked_documents[:k]


def rank_documents_pagerank(query, k=10):
    #####################Task t2k: your code #######################

    #convert query to document using text_to_vec function
    query_as_document = None
    ranked_documents = None
    #Write code for the following:
    #   transform the query using process_text
    #   issue the transformed query to mongodb
    #   get ALL matching documents
    #   order the documents based on their pagerank score (computed in task 3)
    # return top-k documents
    #####################Task t2k: your code #######################
    return ranked_documents[:k]


#Do not change below
def rank_documents(query):
    print "Ranking documents for query:", query
    print "Top-k for TF-IDF"
    print rank_documents_tf_idf(query)
    print "Top-k for Zone Score"
    print rank_documents_zone_scoring(query)
    print "Top-k for Page Rank"
    print rank_documents_pagerank(query)


setup_mongodb()
#####Uncomment the following functions as needed
#process_document_corpus("fileNamesToUUID.txt")
#vocabulary = find_corpus_vocabulary("processedFileNamesToUUID.txt")
#corpus_to_document_vec("vocabulary.txt", "processedFileNamesToUUID.txt", "tf_idf_vector.txt")
