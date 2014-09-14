'''
Created on Mar 8, 2014

@author: Nirmalkumar
'''
import operator

def Precision(selected_doc,expected_doc):
    tp = 0.0 
    for doc in selected_doc:
        if doc in expected_doc:
            tp = tp + 1.0
    
    return tp/len(selected_doc)

def Recall(selected_doc,expected_doc):
    tp = 0.0 
    for doc in selected_doc:
        if doc in expected_doc:
            tp = tp + 1.0
    
    return tp/len(expected_doc)
    
def F1(selected_doc,expected_doc):
    F1 = 0.0
    P = Precision(selected_doc,expected_doc)
    R = Recall(selected_doc,expected_doc)
    if P+R != 0.0:
        F1 = (2.0*P*R)/(P+R)
    
    return F1

def MAP(selected_doc,expected_doc):
    total = 0.0
    for i in range (1,len(selected_doc)):
        if  selected_doc[i-1] in expected_doc:
            total = total + Precision(selected_doc[:i], expected_doc)
        
    return (total/len(selected_doc))
        
def get_top_documents(dict,threshold):
    #sort according to value
    sorted_doc = sorted(dict.iteritems(), key=operator.itemgetter(1) , reverse=True)
    top_doc_lst  = [int(i[0]) for i in sorted_doc]
    return top_doc_lst[:threshold]
    
def call_metrix(dict,expected_doc,threshold):
    '''
    return a tupule
    with four values (precision,recall,F1,Map)
    '''
    selected_doc = get_top_documents(dict,threshold)
    #print selected_doc
    p   = Precision(selected_doc,expected_doc)
    r   = Recall(selected_doc,expected_doc)
    f1  = F1(selected_doc,expected_doc)
    map = MAP(selected_doc,expected_doc)
    
    return (p,r,f1,map)
    
def getMetrics(query_result_lst,rel_dict,doc_threshold):
    """
    input = list of dict
    output = four mertics
    """
    total_queries = len(query_result_lst)
    p = 0.0
    r = 0.0
    f1= 0.0
    map= 0.0
    query_num = 0
    
    for res_dict in query_result_lst:
        t = call_metrix(res_dict,rel_dict[query_num],doc_threshold)
        query_num = query_num + 1
        p = p + t[0]
        r = r + t[1]
        f1 = f1 + t[2]
        map = map + t[3]
    
    p = p / total_queries
    r = r / total_queries
    f1 = f1/total_queries
    map = map/total_queries
    
    return (p,r,f1,map)
            