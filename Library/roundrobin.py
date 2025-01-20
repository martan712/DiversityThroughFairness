import copy 

import itertools

def roundrobin(*iterables):
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = itertools.cycle(itertools.islice(iterators, num_active))
        yield from map(next, iterators)
        
def roundRobinWithClusters(ranking, clusters, cluster_preferences, n_clusters=10, l=100):
    order = list(map(lambda x: x[0], sorted(cluster_preferences, key=lambda x: x[1])[::-1]))
    ranking = ranking[:]
    clusters = clusters[:]
    cluster_list = [ [(ranking[x], clusters[x])  for x in range(len(ranking)) if clusters[x]==i] for i in range(n_clusters)]

    ###
    #    Order clusters in terms of BM25
    cluster_list = list(
            map(
                lambda x: sorted(x, key=lambda x: x[0].score, reverse=True), 
                    cluster_list,
               )
    )

    ordered_clusters = []
    rr = []
    ### Take first 5 items ###
    # if len(order) > 0:
    #     rr =  cluster_list[order[0]][:min(len(cluster_list[order[0]]), 5)]
    #     cluster_list[order[0]] = cluster_list[order[0]][min(len(cluster_list[order[0]]), 5):]
    
    for item in order:
        ordered_clusters.append(cluster_list[item])    

    rr += list(roundrobin(*ordered_clusters))

    cluster_list = [cluster_list[x] for x in range(len(cluster_list)) if x not in order]
    remaining_clusters = sum(cluster_list, [])
    remaining_clusters.sort(key=lambda x:x[0].score, reverse=True)

    rr+=remaining_clusters
    return rr[:100]    