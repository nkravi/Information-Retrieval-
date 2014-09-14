""" Assignment 0

You will implement a simple in-memory boolean search engine over the jokes
from http://web.hawkesnest.net/~jthens/laffytaffy/.

The documents are read from documents.txt.
The queries to be processed are read from queries.txt.

Your search engine will only need to support AND queries. A multi-word query
is assumed to be an AND of the words. E.g., the query "why because" should be
processed as "why AND because."
"""
"""  Nirmal kumar Ravi"""

# Some imports you may want to use.
from collections import defaultdict
import re

"""Removes punctuation from the given string and
replaces with a space"""
def remove_punctuation(document):
    tmp_doc = []
    punctuation = [',','.','?','!','(',')',';',':','\'','-','"','`']
    for letter in document.lower():
        if letter in punctuation:
            tmp_doc.append(' ')
        else:
            tmp_doc.append(letter)
    
    return ''.join(tmp_doc)
    
def read_lines(filename):
    """ Read a file to a list of strings. You should not need to modify
    this. """
    return [l.strip() for l in open(filename, 'rt').readlines()]


def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Remove all punctuation and split on whitespace.
    >>> tokenize("Hi there. What's going on?")
    ['hi', 'there', 'what', 's', 'going', 'on']
    """ 
    return remove_punctuation(document).split()
    pass


def create_index(tokens):
    """
    Create an inverted index given a list of document tokens. The index maps
    each unique word to a list of document ids, sorted in increasing order.
    >>> index = create_index([['a', 'b'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [0, 1]
    >>> index['b']
    [0]
    >>> index['c']
    [1]
    """
    dict = {}
    document_id = 0
    for token in tokens:
        for word in token:
            if word not in dict.keys():
                dict[word] = [document_id]
            else:
                tmp = dict[word]
                if document_id not in tmp:
                    tmp.append(document_id)
                dict[word] = tmp
        document_id = document_id+1
    
    return dict
    pass


def intersect(list1, list2):
    """ Return the intersection of two posting lists. Use the optimize
    algorithm of Figure 1.6 of the MRS text.
    >>> intersect([1, 3, 5], [3, 4, 5, 10])
    [3, 5]
    >>> intersect([1, 2], [3, 4])
    []
    """
    result=[]
    i=0
    j=0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i = i+1
            j = j+1
        elif list1[i] < list2[j]:
            i = i+1
        else:
            j= j+1
    return result
    
    pass


def sort_by_num_postings(words, index):
    """
    Sort the words in increasing order of the length of their postings list in
    index.
    >>> sort_by_num_postings(['a', 'b', 'c'], {'a': [0, 1], 'b': [1, 2, 3], 'c': [4]})
    ['c', 'a', 'b']
    """
    tmp_lst=[]
    tmp_index={}
    """
    tmp_lst = sorted(index , key = index.__getitem__)
    tmp_words = words
    """
    for key in index.keys():
        tmp_index[key] = len(index[key])    
    tmp_lst = sorted(tmp_index , key = tmp_index.__getitem__)
    tmp_words = words
    tmp_words.sort(key = lambda x: tmp_lst.index(x))
    return tmp_words
    pass


def search(index, query):
    """ Return the document ids for documents matching the query. Assume that query is a single string, possible containing multiple words. The steps are to:
    1. tokenize the query
    2. Sort the query words by the length of their postings list
    3. Intersect the postings list of each word in the query.
    E.g., below we search for documents containing 'a' and 'b':
    >>> search({'a': [0, 1], 'b': [1, 2, 3], 'c': [4]}, 'a b')
    [1]
    """
    result = []
    tmp_query = tokenize(query)
    if (1 == len(tmp_query)):
       result = index[tmp_query[0]]
    else:
        result = index[tmp_query[0]]
        for word in tmp_query[1:]:
            result = intersect(result,index[word])
    return result         
    pass


def main():
    """ Main method. You should not modify this. """
    
    print create_index([['a', 'a']])
    '''  
    documents = read_lines('documents.txt')
    tokens = [tokenize(d) for d in documents]
    index = create_index(tokens)
    queries = read_lines('queries.txt')
    for query in queries:
        results = search(index, query)
        print '\n\nQUERY:', query, '\nRESULTS:\n', '\n'.join(documents[r] for r in results)
    '''

if __name__ == '__main__':
   #main()
   import doctest
   doctest.testmod()
   
