"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter
import io
import math
from pprint import pprint
from collections import defaultdict

import numpy as np


class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        Each iteration consists of calls to compute_means and compute_clusters.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector)
        See Log.txt for expected output.
        """
        #assign mean vector
        self.mean_vector = documents[0:self.k] #Take first k vectors as a mean
        
        for i in range (0,iters):
            clusters = self.compute_clusters(documents)
            self.mean_vector = self.compute_means(clusters,documents)
        
        #qdd final cluster and document for to print top docs
        self.clusters = clusters
        self.documents = documents
        pass

    def compute_means(self,clusters,documents):
        """ Compute the mean vectors for each cluster (storing the results in an
        instance variable)."""
        sum_of_clusters = defaultdict(lambda: Counter())
        no_of_clusters = defaultdict(lambda: 0)
        error = 0.0
        for cluster in clusters:
            doc_id,culster_id,dist = cluster
            error+= dist #sum of errors of all cluster
            sum_of_clusters[culster_id] += documents[doc_id]
            no_of_clusters[culster_id] += 1
        
        #calculate average 
        res = [] 
        for  cid in sorted(sum_of_clusters.keys()):
            n =  float(no_of_clusters[cid])
            for key in sum_of_clusters[cid].keys():
                sum_of_clusters[cid][key] = sum_of_clusters[cid][key]/n
            res.append(sum_of_clusters[cid])
                
        #print error and number of term in each cluster
        print [n[1]  for n in sorted(no_of_clusters.items())]
        print  error 
        return res
        pass

    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable). """
        mean_norms = self.compute_mean_norms(self.mean_vector) #compute mean norms once for each cluster
        cluster = []
        for i in range(0,len(documents)):
            cluster.append((i,)+ self.min_distance(documents[i],mean_norms))
            
        return cluster
        pass
    
    def compute_mean_norms(self,mean_norms):
        """
        Computer mean norms of all mean vector
        Returns Square of all mean vectors
        """
        res = []
        for mean_norm in mean_norms:
            a = mean_norm.values()
            res.append(np.dot(a,a))
        return res  
        
    def min_distance(self,doc,mean_norms):
        """
        Given a doc , tests its distance
        with all given cluster means and returns 
        """
        distance = []
        for i in range(0,len(self.mean_vector)):
            distance.append((i, self.distance(doc, self.mean_vector[i], mean_norms[i])))
        
        return  self.min(distance) 
        
    def min(self,distance):
        """
        return a minimum value in 
        a list [(clusterId,value)]
        """
        min = distance[0]
        for  d in distance:
            if d[1] < min[1]:
                min = d
        return min
    
    def aDOTb(self,a,b):
        """
        returns dot product of two vectors
        """
        res = 0.0
        for key in b.keys():
            if key in a:
                res += a[key]*b[key]
        return res
        
    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
        #use formulae A*A + B*B -2AB
        A = mean_norm
        tmpB = doc.values()
        B = np.dot(tmpB,tmpB)
        AdotB = self.aDOTb(mean,doc)
        
        distance = math.sqrt(A + B - 2.0*AdotB)
        return distance

    def error(self, documents):
        """ Return the error of the current clustering, defined as the sum of the
        Euclidean distances between each document and its assigned mean vector."""
        """
        implemented in cluster_means
        """
        pass

    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster, sorted by distance to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (which will be out of order from the original
        document).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
        
        clusters = sorted(self.clusters, key=lambda tup: tup[2])
        top_doc = defaultdict(lambda: [])
        for c in clusters:
            doc_id,culster_id,dist = c
            top_doc[culster_id] += [(dist,doc_id)]
        
        for k in sorted(top_doc.keys()):
            count = 0
            print 'CLUSTER  '+str(k)
            for d in sorted(top_doc[k]):
                if count == n:
                    break
                elif len(self.documents[d[1]]) > 3:
                    #print ' '.join((sorted((self.documents[d[1]]).keys())))
                    print ' '.join([unicode(k).encode('utf8') for k in self.documents[d[1]]])
                    #print ' '.join((sorted((self.documents[d[1]]).keys())))
                    #print self.documents[d[1]].keys()
                    count += 1
        
        pass


def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    #total elements in dictionary
    total_terms = Counter()
    for doc in docs:
        total_terms += Counter(doc.keys())
        
    #terms that exceeds threshold
    del_terms = []
    for terms in total_terms.keys():
        if total_terms[terms] < min_df:
            del_terms.append(terms)
    
    #delete terms that are in delete list
    pruned_doc = []
    for doc in docs:
        for term in doc.keys():
            if term in del_terms:
                doc.pop(term)
        if len(doc) > 0: #No need to add empty doc
            pruned_doc.append(Counter(doc))
            
    
    return pruned_doc
    pass


def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with io.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles


def main():
    """ DO NOT MODIFY. """
    #profiles = read_profiles('test.txt')
    profiles = read_profiles('profiles.txt')
    print 'read', len(profiles), 'profiles.'
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()
    #import doctest
    #doctest.testmod()
