""" Assignment 2

You will modify Assignment 1 to support cosine similarity queries.

The documents are read from documents.txt.

The index will store tf-idf values using the formulae from class.

The search method will sort documents by the cosine similarity between the
query and the document (normalized only by the document length, not the query
length, as in the examples in class).

The search method also supports a use_champion parameter, which will use a
champion list (with threshold 10) to perform the search.

"""
from collections import defaultdict
from collections import Counter
import codecs
import math
import re
import operator


class Index(object):

    def __init__(self, filename=None, champion_threshold=10):
        """ DO NOT MODIFY.
        Create a new index by parsing the given file containing documents,
        one per line. You should not modify this. """
        if filename:  # filename may be None for testing purposes.
            self.documents = self.read_lines(filename)
            stemmed_docs = [self.stem(self.tokenize(d)) for d in self.documents]
            self.NWORDS = self.populate_words_for_spell_check(stemmed_docs)
            self.doc_freqs = self.count_doc_frequencies(stemmed_docs)
            self.index = self.create_tfidf_index(stemmed_docs, self.doc_freqs)
            self.doc_lengths = self.compute_doc_lengths(self.index)
            self.champion_index = self.create_champion_index(self.index, champion_threshold)
            
    
   
    def populate_words_for_spell_check(self,docs):
        spell_dic = defaultdict(self.def_dict)
        for doc in docs:
            for word in doc:
                self.add_to_spell_dict(spell_dic,word)
        return spell_dic
                
    def add_to_spell_dict(self,dict,key):
        if self.is_key_present(dict, key):
            dict[key] = dict[key] + 1
        else:
            dict[key] = 1
                
    def edits1(self,word):
       alphabet = 'abcdefghijklmnopqrstuvwxyz'
       splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
       deletes    = [a + b[1:] for a, b in splits if b]
       transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
       replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
       inserts    = [a + c + b     for a, b in splits for c in alphabet]
       return set(deletes + transposes + replaces + inserts)
    
    def known_edits2(self,word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.NWORDS)
    
    def known(self,words): return set(w for w in words if w in self.NWORDS)
    
    def correct(self,word):
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        return max(candidates, key=self.NWORDS.get)
            
    '''
    adds value to compute dictinoary 
    double the key value and add to dict
    '''
    def add_to_compute_dictinoary(self,compute_dict,key,value):
        if self.is_key_present(compute_dict, key):
            compute_dict[key] = compute_dict[key] + value*value
        else:
            compute_dict[key] = value*value
            
        
    
    def compute_doc_lengths(self, index):
        """
        Return a dict mapping doc_id to length, computed as sqrt(sum(w_i**2)),
        where w_i is the tf-idf weight for each term in the document.

        E.g., in the sample index below, document 0 has two terms 'a' (with
        tf-idf weight 3) and 'b' (with tf-idf weight 4). It's length is
        therefore 5 = sqrt(9 + 16).

        >>> lengths = Index().compute_doc_lengths({'a': [[0, 3]], 'b': [[0, 4]]})
        >>> lengths[0]
        5.0
        """
        compute_dict = defaultdict(self.def_dict)
        doc_len_lst = []
        for key in index.keys(): #two level iteration to get the document
            docs = index[key]
            for doc in docs:
                self.add_to_compute_dictinoary(compute_dict, doc[0], doc[1])
        
        for key in sorted(compute_dict.keys()): #takes square root of values and add to list
            compute_dict[key] = math.sqrt(compute_dict[key])
        
      
        return compute_dict
        pass
        
        

    def create_champion_index(self, index, threshold=10):
        """
        Create an index mapping each term to its champion list, defined as the
        documents with the K highest tf-idf values for that term (the
        threshold parameter determines K).

        In the example below, the champion list for term 'a' contains
        documents 1 and 2; the champion list for term 'b' contains documents 0
        and 1.

        >>> champs = Index().create_champion_index({'a': [[0, 10], [1, 20], [2,15]], 'b': [[0, 20], [1, 15], [2, 10]]}, 2)
        >>> champs['a']
        [[1, 20], [2, 15]]
        >>> champs['b']
        [[0, 20], [1, 15]]
        """
        champ_dict = defaultdict(self.def_dict)
        for key in index.keys():
            tmp_lst = index[key]
            tmp_lst = sorted(tmp_lst,key=operator.itemgetter(1),reverse=True) #sort with tf-idf values
            champ_dict[key] = tmp_lst[:threshold] #add to dict till the threshold
        
        return champ_dict
    
        pass
    '''
    Given a document frequency dict convert to idf dict
    formulae used : log10(total_documents/doc_freqs)
    '''    
    def calculate_idf(self,total_documents,doc_freqs):
        idf_dict = defaultdict(self.def_dict)
        for key in doc_freqs.keys():
            idf_dict[key] = math.log((total_documents/doc_freqs[key]),10) 
        
        return idf_dict
    '''   
     Given a list convert it in to term frequency dict
     formulae : 1 + log10wc   where wc - no of times word occurs in document
    '''
    def calculate_term_frequency(self,doc):
        tf_dict = dict(Counter(doc))
        for key in tf_dict.keys():
            tf_dict[key] = 1 + math.log(tf_dict[key],10)
        
        return tf_dict
            
    '''
    adds value to tfidf dict
    '''
    def add_to_tfidf_dictinoary(self,tfidf_dict,key,value):
        if self.is_key_present(tfidf_dict, key):
            tmp_lst = tfidf_dict[key]
            tmp_lst.append(value)
            tfidf_dict[key] = tmp_lst
        else:
            tfidf_dict[key] = [value] #list of list
            
        return
    '''
    cal tfidf by multiplying tf*idf
    '''
    def calculate_tf_idf(self,idf_dict,tf_dict,tfidf_dict,doc_id):
        for key in tf_dict.keys():
            value = [doc_id,idf_dict[key]*tf_dict[key]]
            self.add_to_tfidf_dictinoary(tfidf_dict, key,value)
         
            
                      
    def create_tfidf_index(self, docs, doc_freqs):
        """
        Create an index in which each postings list contains a list of
        [doc_id, tf-idf weight] pairs. For example:

        {'a': [[0, .5], [10, 0.2]],
         'b': [[5, .1]]}

        This entry means that the term 'a' appears in document 0 (with tf-idf
        weight .5) and in document 10 (with tf-idf weight 0.2). The term 'b'
        appears in document 5 (with tf-idf weight .1).

        Parameters:
        docs........list of lists, where each sublist contains the tokens for one document.
        doc_freqs...dict from term to document frequency (see count_doc_frequencies).

        Use math.log10 (log base 10).

        >>> index = Index().create_tfidf_index([['a', 'b', 'a'], ['a']], {'a': 2., 'b': 1., 'c': 1.})
        >>> sorted(index.keys())
        ['a', 'b']
        >>> index['a']
        [[0, 0.0], [1, 0.0]]
        >>> index['b']  # doctest:+ELLIPSIS
        [[0, 0.301...]]
        """
        tfidf_dict = defaultdict(self.def_dict)
        total_num_documents = float(len(docs)) #to get result div/mul in float
       
        idf_dict = self.calculate_idf(total_num_documents, doc_freqs)
        
        for i in range(0,len(docs)):
            tf_dict = self.calculate_term_frequency(docs[i])
            self.calculate_tf_idf(idf_dict, tf_dict, tfidf_dict, i) #where i is doc id
        
        return tfidf_dict
        pass
    '''
    used by default dict in 
    create_positional_index(tokens)
    '''
    def def_dict(self):
        return -1
    '''
    removes duplicates from the given list
    '''
    def remove_duplicates_from_lst(self,lst):
        tmp_lst  = sorted(set(lst))
        return tmp_lst
    '''
    checks whether the dictinoary contains the word
    return true if word is present
    otherwise false
    Note : only for dictinoary which uses def_dict() function
    '''
    def is_key_present(self,dict,word):
        return dict.has_key(word)
    '''
    if word is present increments the word count by one
    else add the word with value one to the dictinoary
    '''
    def count_words_in_doc(self,word_count_dict,doc):
        tmp_doc = self.remove_duplicates_from_lst(doc)
        for word in tmp_doc:
            if self.is_key_present(word_count_dict,word):
                word_count_dict[word] = int(word_count_dict[word]) + 1
            else:
                word_count_dict[word] = 1
            
    def count_doc_frequencies(self, docs):
        """ Return a dict mapping terms to document frequency.
        >>> res = Index().count_doc_frequencies([['a', 'b', 'a'], ['a', 'b', 'c'], ['a']])
        >>> res['a']
        3
        >>> res['b']
        2
        >>> res['c']
        1
        """
        word_count_dict = defaultdict(self.def_dict)
        for doc in docs:
            self.count_words_in_doc(word_count_dict,doc) #used to count the words in each document
        
        return word_count_dict
        pass
    '''
    return a dictinoary of DF for given query
    basically refers to doc_freqs dictinoary
    '''
    def calculate_query_doc_frequency(self,query):
        query_doc_freq = defaultdict(self.def_dict)
        for word in query:
            query_doc_freq[word]=self.doc_freqs[word]
        
        return query_doc_freq
            
        
    def query_to_vector(self, query_terms):
        """ Convert a list of query terms into a dict mapping term to inverse document frequency.
        Parameters:
        query_terms....list of terms
        """
        idf_dict = defaultdict(self.def_dict)
        query_doc_freq = self.calculate_query_doc_frequency(query_terms)
        idf_dict = self.calculate_idf(float(len(self.documents)), query_doc_freq) #idf
       # tf_dict = self.calculate_term_frequency(query_terms)#tf
        
        
        
        return idf_dict
        pass

    def search_by_cosine(self, query_vector, index, doc_lengths):
        """
        Return a sorted list of doc_id, score pairs, where the score is the
        cosine similarity between the query_vector and the document. The
        document length should be used in the denominator, but not the query
        length (as discussed in class). You can use the built-in sorted method
        (rather than a priority queue) to sort the results.

        The parameters are:

        query_vector.....dict from term to weight from the query
        index............dict from term to list of doc_id, weight pairs
        doc_lengths......dict from doc_id to length (output of compute_doc_lengths)

        In the example below, the query is the term 'a' with weight
        1. Document 1 has cosine similarity of 2, while document 0 has
        similarity of 1.

        >>> Index().search_by_cosine({'a': 1}, {'a': [[0, 1], [1, 2]]}, {0: 1, 1: 1})
        [(1, 2), (0, 1)]
        """
        cosine_dict = defaultdict(self.def_dict)
        for q in query_vector.keys():
            cosine_val_query = query_vector[q]
            lst = index[q]
            for l in lst:
                doc_id = l[0]
                cosine_val_doc = l[1]
                cosine_val = cosine_val_doc * cosine_val_query
                if self.is_key_present(cosine_dict, doc_id):
                    cosine_dict[doc_id] = cosine_dict[doc_id]  + cosine_val
                else:
                    cosine_dict[doc_id] = cosine_val
                   
        result_lst = []
        for key in cosine_dict.keys():
            t = (key,cosine_dict[key]/doc_lengths[key])
            result_lst.append(t) #here key is documet ID
              
        return (sorted(result_lst,key=operator.itemgetter(1),reverse=True) )       
        
        
        pass
    '''
    used to tokenize , stem and vectorize query
    return vectorized query
    '''
    def process_query(self,query):
        stemmed_query = self.stem(self.tokenize(query))
        for i in range(0,len(stemmed_query)):
            stemmed_query[i] = self.correct(stemmed_query[i])
        query_to_vector = self.query_to_vector(stemmed_query)
        return query_to_vector
        
    def search(self, query, use_champions=False):
        """ Return the document ids for documents matching the query. Assume that
        query is a single string, possible containing multiple words. Assume
        queries with multiple words are phrase queries. The steps are to:

        1. Tokenize the query (calling self.tokenize)
        2. Stem the query tokens (calling self.stem)
        3. Convert the query into an idf vector (calling self.query_to_vector)
        4. Compute cosine similarity between query vector and each document (calling search_by_cosine).

        Parameters:

        query...........raw query string, possibly containing multiple terms (though boolean operators do not need to be supported)
        use_champions...If True, Step 4 above will use only the champion index to perform the search.
        """
        query_vector = self.process_query(query)
        result_docIds = []
        if use_champions:
            result_docIds = self.search_by_cosine(query_vector, self.champion_index, self.doc_lengths)
        
        else:
            result_docIds = self.search_by_cosine(query_vector, self.index, self.doc_lengths)
            
        return result_docIds
        pass

    def read_lines(self, filename):
        """ DO NOT MODIFY.
        Read a file to a list of strings. You should not need to modify
        this. """
        return [l.strip() for l in codecs.open(filename, 'r', 'utf-8').readlines()]

    def tokenize(self, document):
        """ DO NOT MODIFY.
        Convert a string representing one document into a list of
        words. Retain hyphens and apostrophes inside words. Remove all other
        punctuation and convert to lowercase.

        >>> Index().tokenize("Hi there. What's going on? first-class")
        ['hi', 'there', "what's", 'going', 'on', 'first-class']
        """
        return [t.lower() for t in re.findall(r"\w+(?:[-']\w+)*", document)]

    def stem(self, tokens):
        """ DO NOT MODIFY.
        Given a list of tokens, collapse 'did' and 'does' into the term 'do'.

        >>> Index().stem(['did', 'does', 'do', "doesn't", 'splendid'])
        ['do', 'do', 'do', "doesn't", 'splendid']
        """
        return [re.sub('^(did|does)$', 'do', t) for t in tokens]


def main():
    """ DO NOT MODIFY.
    Main method. Constructs an Index object and runs a sample query. """
    indexer = Index('documents.txt')
    #indexer = Index('testDoc.txt')
    #for query in ['game of life', 'learning']:
    for query in ['pop love song', 'chinese american', 'city']:
        print '\n\nQUERY=', query
        print '\n'.join(['%d\t%e' % (doc_id, score) for doc_id, score in indexer.search(query)[:10]])
        print '\n\nQUERY=', query, 'Using Champion List'
        print '\n'.join(['%d\t%e' % (doc_id, score) for doc_id, score in indexer.search(query, True)[:10]])

if __name__ == '__main__':
    main()
    #import doctest
    #doctest.testmod()
