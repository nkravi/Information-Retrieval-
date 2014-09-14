"""
Assignment 4. Implement a Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

import glob
import math
from collections import defaultdict

class Train(object):
    def __init__(self,documents):
        self.documents = documents
        self.process_doc()
        self.cal_probablity()
                    
    def process_doc(self):
        
        self.word_dict =  defaultdict(lambda: defaultdict(lambda: 0)) #used to store word and a dict[which has class name and times that word occur in that class]
        self.tot_doc_label = defaultdict(lambda : 0) #stores number of classes and doc count that belong to that class
        self.tot_doc_words = defaultdict(lambda : 0) #stores classes and word count in that class
        
        for doc_obj in self.documents:
            self.tot_doc_label[doc_obj.label] += 1
            self.tot_doc_words[doc_obj.label] += len(doc_obj.tokens)
            for token in doc_obj.tokens:
                self.word_dict[token][doc_obj.label] += 1
                
    def cal_probablity(self):
        
        doc_len = len(self.word_dict)
        for token in self.word_dict.keys():
            for label in self.tot_doc_label.keys():
                self.word_dict[token][label] = (self.word_dict[token][label] + 1)/ (float(self.tot_doc_words[label]) + doc_len)
        
        total_doc =  sum(self.tot_doc_label.values())
        for label in self.tot_doc_label.keys():
            self.tot_doc_label[label] = self.tot_doc_label[label]/float(total_doc)
            

                   
                
            
class Document(object):
    """ A Document. DO NOT MODIFY.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename):
        self.filename = filename
        self.label = 'spam' if 'spmsg' in filename else 'ham'
        self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):

    def train(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your book.
        """
        self.trainedDoc = Train(documents)
        """
        t = Train(documents)
        for k in sorted(t.word_dict.keys()):
            for k1 in t.word_dict[k].keys():
                print k , k1 ,  t.word_dict[k][k1]
        
        for k in t.tot_doc_label.keys():
            print k, t.tot_doc_label[k]
        pass
        """
     
    def classify(self, documents):
        """
        TODO: COMPLETE THIS METHOD.

        Return a list of strings, either 'spam' or 'ham', for each document.
        documents....A list of Document objects to be classified.
        """
        
        
        res_doc_label = []
        for doc_obj in documents:
            class_label =  defaultdict(lambda: 0)
            max = 0.00
            doc_class = ''
            for token in doc_obj.tokens:
                if token in self.trainedDoc.word_dict.keys():
                    #print self.trainedDoc.word_dict[token]
                    for label in self.trainedDoc.word_dict[token].keys():
                        class_label[label] = class_label[label] + math.log(self.trainedDoc.word_dict[token][label])
                        #print class_label['ham']
                
                else: #unknown words
                    #print token
                    for label in self.trainedDoc.tot_doc_label.keys():
                        class_label[label] = class_label[label] + math.log( (1.00/(self.trainedDoc.tot_doc_label[label] + (len(self.trainedDoc.word_dict)+1.00))))
                        #print  'class' + str(class_label[label])
                        
            #print 'spam-ham'
            #print class_label['ham'],class_label['spam']
            for label in class_label.keys():
                class_label[label] = class_label[label] + math.log(self.trainedDoc.tot_doc_label[label])
                #doc_class = label
                #max = class_label[label]
                """
                if  class_label[label] > max:
                    max = class_label[label]
                    doc_class = label
                """
            #print class_label['ham'],class_label['spam']
            doc_class = 'ham' if class_label['ham'] > class_label['spam'] else 'spam'
            #print doc_class
            res_doc_label.append(doc_class)
            
            
            
        
        #print res_doc_label
        return res_doc_label
        pass


def evaluate(predictions, documents):
    """
    TODO: COMPLETE THIS METHOD.

    Evaluate the accuracy of a set of predictions.
    Print the following:
    accuracy=xxx, yyy false spam, zzz missed spam
    where
    xxx = percent of documents classified correctly
    yyy = number of ham documents incorrectly classified as spam
    zzz = number of spam documents incorrectly classified as ham

    See the provided log file for the expected output.

    predictions....list of document labels predicted by a classifier.
    documents......list of Document objects, with known labels.
    """
    flase_spam = 0
    false_ham = 0
    correlcty_classified = 0
    for i in range(0,len(documents)):
        if documents[i].label == predictions[i] :
            correlcty_classified += 1
        else:
            if predictions[i] == 'spam':
                flase_spam += 1
            else:
                false_ham += 1
    
    print 'accuracy\t' + str(correlcty_classified/float(len(documents)))
    print 'false spam\t' + str(flase_spam)
    print 'missed spam\t' + str(false_ham)
    
                
            
            


def main():
    """ DO NOT MODIFY. """
    train_docs = [Document(f) for f in glob.glob("train/*.txt")]
    print 'read', len(train_docs), 'training documents.'
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(f) for f in glob.glob("test/*.txt")]
    print 'read', len(test_docs), 'testing documents.'
    predictions = nb.classify(test_docs)
    evaluate(predictions, test_docs)

if __name__ == '__main__':
    main()
