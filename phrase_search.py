""" Assignment 1

You will modify Assignment 0 to support phrase queries instead of AND queries.

The documents are read from documents.txt.
The queries to be processed are read from queries.txt.

Assume all multi-word queries are phrase queries. E.g., the query "why did
the" should be processed as a phrase, not a conjunction.

In addition, you will modify the tokenize method to keep hyphens and
apostrophes inside words, as well as add a stem method to collapse the terms
"did" and "does" to "do."  (More details are in the comments of each method.)

Finally, complete the find_top_bigrams method to find the most frequent
bigrams of (normalized) terms in the document set.

"""
from collections import defaultdict
import re
import operator



def read_lines(filename):
    """ Read a file to a list of strings. You should not need to modify
    this. """
    return [l.strip() for l in open(filename, 'rt').readlines()]

'''
Given a single word removes 
punctuation at end and start of the word
and converts the word to lower case
'''
def remove_punctuation(word):
    punctuation = [',','.','?','!','(',')',';',':','\'','-','"','`']
    while word[0]  in punctuation or word[-1]  in punctuation: #iterate until all punctuation are removed
        if(word[0] in punctuation): #removes at the start
            word = word[1:]
        if(word[-1] in punctuation): #removes at the end
            word = word[:-1]
            
    return (word.lower())
        
        
def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Retain hyphens and apostrophes inside words. Remove all other
    punctuation and convert to lowercase.

    >>> tokenize("Hi there. What's going on? first-class")
    ['hi', 'there', "what's", 'going', 'on', 'first-class']
    """
    lst_tokenize = []
    for word in document.split():
        lst_tokenize.append(remove_punctuation(word))
    
    return lst_tokenize


def stem(tokens):
    """
    Given a list of tokens, collapse 'did' and 'does' into the term 'do'.

    >>> stem(['did', 'does', 'do', "doesn't", 'splendid'])
    ['do', 'do', 'do', "doesn't", 'splendid']
    """
    for i in range(0,len(tokens)): #iterate through the list replace did and does to do
        if tokens[i] == 'does' or tokens[i] == 'did':
            tokens[i] = 'do'
    
    return tokens


def is_doc_present(doc_id,lst):
    for l in lst:
        if l[0] == doc_id:
            return lst.index(l)
        if doc_id < l[0]:
            return -1
    return -1
        
def add_word_to_dict(indexdict,word,doc_id,word_id):
    if indexdict[word] != -1: #word is  there in dictinoary
        tmp_lst = indexdict[word] #returns a list of list of indexes
        index_to_be_inserted = is_doc_present(doc_id,tmp_lst)
        if index_to_be_inserted != -1: #the document has already got a entry in dict
            #(tmp_lst[doc_id]).append(word_id) #search for the document and append word in it
            tmp_in_lst=tmp_lst[index_to_be_inserted]
            tmp_in_lst.append(word_id)
            tmp_lst[index_to_be_inserted] = tmp_in_lst
        else: #now we have to append both doc_id and word_id
            tmp_lst.append([doc_id,word_id])
    else: #we have to put a fresh entry as no entry is available
       indexdict[word] = [[doc_id,word_id]] 
        
        
        

def process_document(indexdict,doc,doc_id):
    word_id = 0
    for word in doc:
        add_word_to_dict(indexdict,word,doc_id,word_id)
        word_id = word_id + 1

'''
used by default dict in 
create_positional_index(tokens)
'''
def def_dict():
    return -1
       
def create_positional_index(tokens):
    """
    Create a positional index given a list of normalized document tokens. Each
    word is mapped to a list of lists (using a defaultdict). Each sublist
    contains [doc_id position_1 position_2 ...] -- this indicates the document
    the word appears in, as well as the word offset of each occurrence.

    >>> index = create_positional_index([['a', 'b', 'a'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [[0, 0, 2], [1, 0]]
    >>> index['b']
    [[0, 1]]
    >>> index[('c')]
    [[1, 1]]
    """
    indexdict = defaultdict(def_dict)
    doc_id = 0
    for doc in tokens:
        process_document(indexdict,doc,doc_id)
        doc_id = doc_id + 1
    
    return indexdict

def compare_document_postings(list1,list2):
    result=[]
    i=0
    j=0
    while i < len(list1) and j < len(list2):
        if (int(list1[i])+1) == list2[j]:
            result.append(list2[j])
            i = i+1
            j = j+1
        elif list1[i] < list2[j]:
            i = i+1
        else:
            j= j+1
    
    return result
    
def compare_documents(list1,list2):
    result=[]
    i=0
    j=0
    while i < len(list1) and j < len(list2):
        if list1[i][0] == list2[j][0]:
            tmplst = compare_document_postings(list1[i][1:],list2[j][1:])
            if len(tmplst) != 0:
                result.append(([list2[j][0]]+tmplst))
            i = i+1
            j = j+1
        elif list1[i][0] < list2[j][0]:
            i = i+1
        else:
            j= j+1
    
    return result

def phrase_intersect(list1, list2):
    """ Return the intersection of two positional posting lists. A match
    requires a position in list1 to be one less than a position in list2 in
    the same document.

    Your implementation should be linear in the length of the number of
    positions in each list. That is, you should access each position value at
    most once.

    In the example below, word1 occurs in document 0 (positions 1,4), document
    1 (position 0), and document 10 (positions 2, 3, 4). Word2 occurs in
    document 0 (positions 2, 6), document 1 (position 2), document 2 (position
    0), and document 10 (position 1, 5). Thus, the phrase "word1 word2" occurs
    in document 0 (position 1->2) and in document 10 (position 4->5).

    >>> phrase_intersect([[0, 1, 4], [1, 0], [10, 2, 3, 4]], \
                         [[0, 2, 6], [1, 2], [2, 0], [10, 1, 5]])
    [[0, 2], [10, 5]]
    >>> phrase_intersect([[1, 2]], [[1, 4]])
    []
    """
    return compare_documents(list1,list2)
    

def get_document_id(lst):
    result = []
    for l in lst:
        result.append(l[0])
    
    return result
    
        

def search(index, query):
    """ Return the document ids for documents matching the query. Assume that
    query is a single string, possible containing multiple words. Assume
    queries with multiple words are phrase queries. The steps are to:

    1. Tokenize the query
    2. Stem the query tokens
    3. Intersect the positional postings lists of each word in the query, by
    calling phrase_intersect.

    E.g., below we search for documents containing the phrase 'a b c':
    >>> search({'a': [[0, 4], [1, 1]], 'b': [[0, 5], [1, 10]], 'c': [[0, 6], [1, 11]]}, 'a b')
    [0]
    """
    result = []
    tmp_query = stem(tokenize(query))
    if len(tmp_query) == 1 :#if it is a single word query no phrase intersect required a
        if index[tmp_query[0]] != -1:#result should be in dictinoary
            result.append(index[tmp_query[0]]) 
    else: 
        tmp = phrase_intersect(index[tmp_query[0]],index[tmp_query[1]]) 
        for i in range(2,len(tmp_query)):
            #result.append(phrase_intersect(index[tmp_query[i]],index[tmp_query[i+1]]))
            tmp = phrase_intersect(tmp,index[tmp_query[i]])
        
        result.append(tmp)
    
    tmp_lst = []
    for r in result:
        tmp_lst = tmp_lst + get_document_id(r)
    return (list(set(tmp_lst)))    #to remove duplicates in the list
    pass
'''
add word to dictionary
'''
def add_to_biagram_dict(dict,word1,word2):
    word = word1+' '+word2
    if dict[word] == -1: #word not present
        dict[word] = 1
    else:
        value = dict[word]
        dict[word] = value+1
        
'''
Given a list generates the biagrams and add to dict
'''
def generate_biagrams(dict,lst):
    for i in range(0,len(lst)-1):
        add_to_biagram_dict(dict,lst[i],lst[i+1])
        
def find_top_bigrams(terms, n):
    """
    Given a list of lists containing terms, return the most frequent
    bigrams. The return value should be a list of tuples in the form (bigram,
    count), in descending order, limited to the top n bigrams. In the example
    below, there are two documents provided; the top two bigrams are 'b c' (3
    occurrences) and 'a b' (2 occurrences).

    >>> find_top_bigrams([['a', 'b', 'c', 'd'], ['b', 'c', 'a', 'b', 'c']], 2)
    [('b c', 3), ('a b', 2)]
    """
    dict = defaultdict(def_dict)
    for lst in terms:
        generate_biagrams(dict,lst)
    
    sorted_elements = sorted(dict.iteritems(), key=operator.itemgetter(1),reverse=True)
    return sorted_elements[:n]
    pass


def main():
    """ Main method. You should not modify this. """
    documents = read_lines('documents.txt')
    terms = [stem(tokenize(d)) for d in documents]
    index = create_positional_index(terms)
    queries = read_lines('queries.txt')
    for query in queries:
        results = search(index, query)
        print '\n\nQUERY:', query, '\nRESULTS:\n', '\n'.join(documents[r] for r in results)

    print '\n\nTOP 11 BIGRAMS'
    print '\n'.join(['%s=%d' % (bigram, count) for bigram, count in find_top_bigrams(terms, 11)])

  
if __name__ == '__main__':
    main()
    #import doctest
    #doctest.testmod()
