""" Assignment 6: PageRank. """
from collections import defaultdict
import glob
import os
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
# downloaded from http://www.crummy.com/software/BeautifulSoup/bs4/doc/

def parse(folder, inlinks, outlinks):
    """
    Read all .html files in the specified folder. Populate the two
    dictionaries inlinks and outlinks. inlinks maps a url to its set of
    backlinks. outlinks maps a url to its set of forward links.
    """
    dir_path = '.\\'+folder+'\\*.html'
    for filePath in glob.glob(dir_path):
        with open(filePath, 'r') as f:
            html =  f.readlines()
            inlink = f.name.split('\\')[-1] #file which is being read
            b= BeautifulSoup(''.join(html))
            for link in b.find_all('a'):
                outlink = link.get('href')
                outlinks[inlink].add(outlink)
                inlinks[outlink].add(inlink)
    pass


def compute_rw(pr,outlinks,rw):
    for url in pr:
        rw[url] = pr[url]/len(outlinks[url]) #R(V)/|FV}
        
def initialize_pagerank(urls,pr):
    for url in urls:
        pr[url]  = 1.0 

def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    """ Return a dictionary mapping each url to its PageRank.
    The formula is R(u) = 1-b + b * (sum_{w in B_u} R(w) / (|F_w|)

    Initialize all scores to 1.0
    """
    rw = defaultdict(lambda: 0.0)
    pr = defaultdict(lambda: 1.0)
    initialize_pagerank(urls,pr)
    for i in range(0,iters):
        compute_rw(pr,outlinks,rw)
        for url in urls:
            sum = 0.0
            for link in inlinks[url]:
                sum += rw[link]
            pr[url] = 1.0-b+b*sum
                
            
    return pr
    pass


def run(folder, b):
    """ Do not modify this function. """
    inlinks = defaultdict(lambda: set())
    outlinks = defaultdict(lambda: set())
    parse(folder, inlinks, outlinks)
    urls = sorted(set(inlinks) | set(outlinks))
    ranks = compute_pagerank(urls, inlinks, outlinks, b=b)
    print 'Result for', folder, '\n', '\n'.join('%s\t%.3f' % (url, ranks[url]) for url in sorted(ranks))


def main():
    """ Do not modify this function. """
    run('set1', b=.5)
    run('set2', b=.85)


if __name__ == '__main__':
    main()
