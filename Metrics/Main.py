'''
Created on Mar 7, 2014

@author: Nirmalkumar
'''
import Utilities
import TFIDF
import Search
import Metrics
#from tabulate import tabulate



def process_documents():
    '''Read From Document'''
    documents = Utilities.read_from_time_all()
    #documents = read_lines()
    '''Tokens and Stem Documents'''
    documents = Utilities.tokenize_stem_docs(documents)
    '''calculate doc lengths'''
    doc_len = Utilities.calculate_doc_len(documents)
    ''' term frequency'''
    tf = TFIDF.term_frequency(documents)
    '''calculates tf-idf'''
    tfidf = TFIDF.TFIDF(len(documents), tf)
    '''Read From Document'''
    queries = Utilities.read_from_time_que()
    #queries = ['pop love song', 'chinese american', 'city']
    '''Tokens and Stem Documents'''
    queries = Utilities.tokenize_stem_docs(queries)
    
    
    #print Search.search_by_cosine(tfidf,len(documents),['CARTOONISTS'.lower()])
    
    
    cosine_result = []
    rsv_result = []
    BM25_1_5 = []  #b=1 k= 0.5
    BM25_1_1 = [] #b=1 k= 1
    BM25_2_5 = [] #b=2 k= 0.5
    BM25_2_1 = [] #b=2 k= 1 
    
    
    for query in queries:
        cosine_result.append(Search.search_by_cosine(tfidf,len(documents),query))
        rsv_result.append(Search.search_by_rsv(tf,len(documents),query))
        BM25_1_5.append(Search.search_by_BM25(tf,doc_len,query,1.0,0.5))
        BM25_1_1.append(Search.search_by_BM25(tf,doc_len,query,1.0,1.0))
        BM25_2_5.append(Search.search_by_BM25(tf,doc_len,query,2.0,0.5))
        BM25_2_1.append(Search.search_by_BM25(tf,doc_len,query,2.0,1.0))
    
    #print cosine_result[1]
    '''
    read from time.rel
    '''    
    rel_dict = Utilities.read_from_time_rel()
    '''
    print result
    '''
    result = []

    result.append(('System','Precision','Recall','F1','MAP')) 
    result.append( ('cosine  ',) + Metrics.getMetrics(cosine_result,rel_dict,20)) #limit to top 20 search
    result.append( ('RSV  ',) + Metrics.getMetrics(rsv_result,rel_dict,20))
    result.append(('BM25 (1, .5) ',)+ Metrics.getMetrics(BM25_1_5,rel_dict,20))
    result.append(('BM25 (1, 1) ',)+Metrics.getMetrics(BM25_1_1,rel_dict,20))
    result.append(('BM25 (2, .5) ',)+Metrics.getMetrics(BM25_2_5,rel_dict,20)) 
    result.append(('BM25 (2, 1) ',)+Metrics.getMetrics(BM25_2_1,rel_dict,20))
    
    Utilities.tabulate(result)
    Utilities.plot_graph(result)
    
     
    

if __name__ == '__main__':
    process_documents()