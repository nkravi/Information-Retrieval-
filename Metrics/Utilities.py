'''
Created on Mar 7, 2014

@author: Nirmalkumar
'''
import re
from collections import defaultdict
import sys
import matplotlib.pyplot as plt


def read_from_time_all():
    '''
    this function is customized read for TIME.ALL
    return a list of documents
    '''
    return read_file_with_astreik_as_delimiter('./time/TIME.ALL')

def read_from_time_que():
    '''
    this function is customized read for TIME.QUE
    return a list of documents
    '''
    return read_file_with_astreik_as_delimiter('./time/TIME.QUE')
   
def read_from_time_rel():
    '''
    this function is customized read for TIME.QUE
    return a dictionary with query-id as key and list of values
    '''
    rel_dict = defaultdict(lambda: -1)
    with open('./time/TIME.REL','r') as f:
        for line in f:
            if len(line.strip()) >0:
                line = line.strip().split()
                line[:] = [int(x) - 1 for x in line] #subtract one from all values to index with zero
                rel_dict[line[0]] = line[1:]
    
    return rel_dict
                
                
    
def read_file_with_astreik_as_delimiter(filePath):
    '''
    this function reads the file with (*) as delimiter
    return a list of documents
    '''
    documents= []
    doc=''
    with open(filePath,'r') as f:
        for line in f:
            if  line.startswith(r"*") and len(doc) > 0: #'*' is a delimiterr here
                documents.append(doc)
                doc=''
                continue
            if not len(line.strip()) == 0 and not line.startswith(r"*"):
                doc= doc+line
    return documents
    

def tokenize(document):
    """ 
    Convert a string representing one document into a list of
    words. Retain hyphens and apostrophes inside words. Remove all other
    punctuation and convert to lowercase.
    """
    return [t.lower() for t in re.findall(r"\w+(?:[-']\w+)*", document)]

def stem(tokens):
    """ 
    Given a list of tokens, collapse 'did' and 'does' into the term 'do'.
    """
    return [re.sub('^(did|does)$', 'do', t) for t in tokens]

def tokenize_stem_docs(documents):
    """
    Given a list of documents tokenize and stem those documents
    """
    return [stem(tokenize(d)) for d in documents]

def remove_duplicates_from_lst(lst):
        """
        Given a list removes duplicate from 
        the list and returns it
        Warning: List is sorted which may cause change in order of 
        elements in the list
        """
        return sorted(set(lst))
    
def is_key_present(dict,key):
    """
    returns true if key is present
    Warning : works only when dict created 
    with  defaultdict(lambda: -1)
    """
    return dict.has_key(key)
       

def add_to_dictinoary(dict,key,value):
    '''
    given key/value adds it to dictionary
    if key is present add the value 
    to it else put a new entry
    '''
    if is_key_present(dict,key):
        dict[key] = dict[key] + value
    else:
         dict[key] = value
        
    
    
def add_key_and_increment_value_by_one(dict,key):  #no need
    """
    If word is present in the dict
    increment the current value by one
    Else add new word with one
    """
    add_to_dictinoary(dict,key,1)
    
def calculate_doc_len(docs):
    """
    Given a list of documents
    calculates the lenght of the document
    and returns a dictinoary with doc-id as
    key and doc-len as value
    """
    doc_len_dict = defaultdict(lambda: -1)
    doc_id =0 
    for doc in docs:
        doc_len_dict[doc_id] = len(doc)
        doc_id = doc_id + 1
    
    return doc_len_dict

def calculate_mean(dict):
    """
    given a dictinoary
    calculates mean of all it values
    """
    return (sum(dict.values())/float(len(dict)))

def leave_space(str,size):
    l = len(str)
    l = size-l
    return str+' '*l

def tabulate(lst):
    for l in lst:
        sys.stdout.write('\n')
        for t in l:
            sys.stdout.write(leave_space(str(t),20))

def plot_graph(lst):
    p = []
    r = []
    for l in lst[1:]:
        p.append(l[1])
        r.append(l[2])
    
    plt.xlabel('Precision')
    plt.ylabel('Recall')
    plt.plot(p,r,'ro')
    plt.show()