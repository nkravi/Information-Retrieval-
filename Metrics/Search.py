'''
Created on Mar 7, 2014

@author: Nirmalkumar
'''
import Utilities
import math
import TFIDF
from collections import defaultdict


def search_by_cosine(tfidf_dict,total_documents,query):
    """
    calculate cosine value given a query
    return dictionary of related documents 
    with its cosine value
    """
    docs_cosine_value = defaultdict(lambda: -1)
    doc_len = normalize_doc_len_for_cosine(tfidf_dict) #normalize doc lengths
    query_idf = calculate_idf_for_query(tfidf_dict,total_documents,query)
    
    for query_word in query_idf.keys():
        for doc_id in tfidf_dict[query_word].keys():
            cosine_value_of_doc = ((tfidf_dict[query_word][doc_id] * query_idf[query_word]) / doc_len[doc_id])
            Utilities.add_to_dictinoary(docs_cosine_value,doc_id,cosine_value_of_doc)
    
    return docs_cosine_value
             
            
def calculate_idf_for_query(tfidf_dict,total_documents,query):
    """
    used to calculate idf values 
    of the query - just a look up in tfidf_dict/tf dict
    for doc-frequency and calculate idf
    """
    query_idf = defaultdict(lambda: -1)
    for word in query:
        if Utilities.is_key_present(tfidf_dict,word):#if query term present in our dictionary        
            word_idf = TFIDF.cal_idf(float(total_documents),len(tfidf_dict[word]))
            Utilities.add_to_dictinoary(query_idf,word,word_idf)
    
    return query_idf
         
    
def normalize_doc_len_for_cosine(tfidf_dict):
    """
    normalize the doc len for 
    cosine calculation square tf-idf and 
    takes the square-root of related documents with term
    """
    doc_len = defaultdict(lambda: -1)
    for word in tfidf_dict.keys():
        for doc_id in tfidf_dict[word].keys():
            value = tfidf_dict[word][doc_id] * tfidf_dict[word][doc_id] #square the value
            Utilities.add_to_dictinoary(doc_len,doc_id,value)
    
    for key in doc_len.keys(): #taking square root
        doc_len[key] = math.sqrt(doc_len[key]) 
    
    
    return doc_len
        

def search_by_rsv(tf_dict,total_documents,query):
    """

    """
    query_idf = calculate_idf_for_query(tf_dict,total_documents,query)
    docs_rsv_value = defaultdict(lambda: -1)
    for query_word in query_idf.keys():
        for doc_id in tf_dict[query_word].keys():
            value = tf_dict[query_word][doc_id] * query_idf[query_word] #tf*IDF #TF not normalized
            Utilities.add_to_dictinoary(docs_rsv_value,doc_id,value)
    
    return docs_rsv_value

def score(k, b, tf, length, m_length):
    return (k + 1) * tf / (k * ((1 - b) + b * length / m_length) + tf)
            
def search_by_BM25(tf_dict,doc_len_dict,query,B,K):
    """
    """
    total_documents = len(doc_len_dict)
    query_idf = calculate_idf_for_query(tf_dict,total_documents,query)
    doc_mean = Utilities.calculate_mean(doc_len_dict)
    
    docs_BM25_value = defaultdict(lambda: -1)
    
    for query_word in query_idf.keys():
        for doc_id in tf_dict[query_word].keys():
            value = score(K,B,tf_dict[query_word][doc_id],doc_len_dict[doc_id],doc_mean) * query_idf[query_word] #tf*IDF #TF not normalized
            Utilities.add_to_dictinoary(docs_BM25_value,doc_id,value)
            
    return  docs_BM25_value
    
    
    