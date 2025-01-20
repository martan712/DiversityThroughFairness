from pyserini.index import IndexReader
from pyserini.search.lucene import LuceneSearcher
import pandas as pd
import json

datapath = "."

class Searcher():
    index_reader = IndexReader(f'{datapath}/data/indexes/indexes/lucene-index')
    searcher = LuceneSearcher(f"{datapath}/data/indexes/indexes/lucene-index")
    with open(f"{datapath}/queries.json", "r") as file:
        queries = pd.DataFrame(json.load(file))
        assert( set(queries.columns) == set(['id', 'keywords', 'title', 'rel_docs', 'URL']) )
        # transform string to list
        queries["rel_docs"]= list(map(lambda x: x.strip('][').split(', '), queries["rel_docs"]))
        # check type
        assert(type(queries["rel_docs"][0]) == list)

    def __init__(self):
        pass

    def search(self, s, e, k=500, verbose=True, expand= False):
        # s is our starting query
        # e is our final query
        # k is the number of results we want to gather for each query

        ###
        # itterate over rows s until e
        # extract information from our queries table
        # return the list of combined results and relevancy labels
        ###
        
        results = []
        

        for _, row in self.queries[s:e].iterrows():
            project = row["title"]
            q   = row["keywords"]
            r   = row["rel_docs"]
                        
            if verbose:
                print(project)
                
            topH = self.searcher.search(q, k=k)

            results.append( ([doc for doc in topH], r) )
            
        return results