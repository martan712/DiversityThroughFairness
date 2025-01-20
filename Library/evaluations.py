import numpy as np 
import math 
from scipy.spatial.distance import jensenshannon

from Library.fairness import *

def get_relevancy_labels(ranking, rel_judge):
    return [1 if x.docid in rel_judge else 0 for x in ranking]

def DCG(query_relevancy_labels, k):
    l = len(query_relevancy_labels)
    return np.sum(
        [0 if j == 0 else i / j for i, j in zip(query_relevancy_labels[:k], [math.log(2+i,2) for i in range(min(k, l))])]
    )
    
def NDCG(query_relevancy_labels, k):
    #ideal = np.sort(query_relevancy_labels)[::-1]
    #print(ideal)
    ideal = [1]*k
    return 0 if DCG(ideal, k) == 0 else DCG(query_relevancy_labels, k)/DCG(ideal, k)

def J(document_topics, topic, alpha=0.5):
    d = dict(document_topics)
    if topic in d.keys():
        return d[topic] #should this be alpha?
    else:
        return 0

def r_i(i, clustering_topics_so_far):
    return sum([ J(j, i) for j in clustering_topics_so_far])
    
def gain(k, clustering_topics, alpha = 0.5, n_topics = 10):
    # gain for document k, with 
    cluster_topics = list(clustering_topics)[:]
    d_k = cluster_topics[k]
    k_prev = cluster_topics[:k]
    if k == 0:
        return  sum([J(d_k, i) for i in range(n_topics)])
    else:
        #print( [(J(d_k, i), r_i(i, k_prev)) for i in range(n_topics)])
        return sum(
            [ J(d_k, i) * (1 - alpha)**(r_i(i, k_prev)) for i in range(n_topics)]
        )

def DCG_2(clustering_topics, k):
    return sum( 
        [ 
            (gain(k, clustering_topics[:k+1])/ (math.log2(2 + k)))
            for k in range(min( len(clustering_topics), k))
        ]
    )

def get_max_gain_element(current_list, items):
    max_gain = 0
    max_index = None
    
    current_list = current_list[:]
    k = len(current_list) 
    
    for i, item in enumerate(items):
        lst = current_list[:]
        lst.append(item)
        new_gain = gain(k, lst)
        if new_gain > max_gain:
            max_index = i
            max_gain = new_gain

    return max_index

def ideal(clustering_topics, k):
    clustering_topics = clustering_topics[:]
    ideal = []
    size = min(len(clustering_topics), k)
    while len(ideal) < size:
        max_index = get_max_gain_element(ideal, clustering_topics)
        max_element = clustering_topics.pop(max_index)
        #print(gain_list, max_index, max_element)
        ideal.append(max_element)
    return ideal


def NDCG_2(clustering_topics, k):
    return DCG_2(clustering_topics, k)/DCG_2(ideal(clustering_topics, k), k)

def get_topic_info_reranking(clustering_topics, ranking, reranking):
    rr =  [x.docid for x in ranking]
    return [ clustering_topics[rr.index(y)] for y in [x.docid for x in reranking]] 

def get_fairness_NDCG(ranking):
    try:
        fairness = get_fairness(ranking)
    except:
        fairness = get_fairness2(ranking)
    for k, item in enumerate(ranking):
        try:
            fairness.loc[eval(item.docid)]/= math.log2(max(k, 2))
        except:
            True
    return fairness.sum()

def JS(r1, r2):
    return 1- jensenshannon(r1, r2, 2.0)