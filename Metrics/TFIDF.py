'''
Created on Mar 7, 2014

@author: Nirmalkumar
'''
from collections import defaultdict
import Utilities
import math
from copy import deepcopy


def document_frequency(documents):                               #Not used as of now
    '''
    Given a list of documents calculate
    the document frequency
    returns a dictionary with word as key and
    its document frequency as value
    '''
    
    document_frequency_dict = defaultdict(lambda: -1)
    
    for doc in documents:
        doc = Utilities.remove_duplicates_from_lst(doc)
        for word in doc:
            Utilities.add_to_dictinoary(document_frequency_dict,word,1)
            
    return document_frequency_dict



def cal_idf(N,doc_freq):
    '''
    used by TFIDF to 
    to calculate  idf
    '''
    return math.log((float(N)/doc_freq),10) 

def term_frequency(documents):
    '''
    Given a list of documents calculate 
    term frequency
    return a dictionary with word as key and 
    term dictionary as value
    term dictionary contains document id and no of
    times the term occurs in the document
    '''
    
    term_frequency_dict = defaultdict(lambda: -1)
    doc_id = 0
    for doc in documents:
        for word in doc:
            if not Utilities.is_key_present(term_frequency_dict,word):#dict is not  present
                term_dict = defaultdict(lambda: -1)                   #create dict
                term_frequency_dict[word] = term_dict
                
            Utilities.add_to_dictinoary(term_frequency_dict[word],doc_id,1)
        
        doc_id = doc_id + 1 #increment doc-id
    
    return term_frequency_dict
                


def TFIDF(N,term_frequency):
    '''
    given a list of documents calculates TFIDF
    uses term_frequency to count terms
    return TFIDF_dict with 
    term as key and dict as value
    the value dict contains doc-id and corresponding
    tf-idf
    '''
    '''
    N = len(documents)
    TFIDF_dict = term_frequency(documents)
    '''
    TFIDF_dict = deepcopy(term_frequency)
    for key in TFIDF_dict.keys():
        term_dict = TFIDF_dict[key]
        idf = cal_idf(float(N),len(term_dict)) #calculating IDF
        for innerkey in term_dict.keys():
            term_dict[innerkey] = (1 + math.log(term_dict[innerkey],10)) * idf #tf-idf = term frequency* idf
    
    
    return TFIDF_dict
            
            
    

    
    

                
                
                
                