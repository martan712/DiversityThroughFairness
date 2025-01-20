def cluster():
    import csv
clusterings = []
clustering_preferences = []
clustering_topics = []

version = "500items_10_clusters"
file = f"clusters/clusterings{version}.csv"
file2 = f"clusters/clustering_preferences{version}.csv"
file3 = f"clusters/clustering_topics{version}.csv"
if not (os.path.isfile(file)):
    
    for i, ranking in enumerate(tqdm(rankings_total)):
        clusters, preferences, topics = get_clustering(ranking, ranking_index=i, searcher=searcher)
        
        clusterings.append(clusters)
        clustering_preferences.append(preferences)
        clustering_topics.append(list(topics))
        
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(clusterings)

    with open(file2, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(clustering_preferences)

    with open(file3, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(clustering_topics)

else:
    with open(file) as f:
        clusterings = list(
            map(lambda x: x.split(","), f.read().splitlines())
        )
        clusterings = list(
            map( lambda x: list(map( lambda y: eval(y), x)), clusterings)
        )
    with open(file2) as f:
        lines = f.read()
        clustering_preferences= list(
            csv.reader(lines.splitlines())
        )
    
        clustering_preferences = list(
            map( lambda x: list(map( lambda y: eval(y), x)), clustering_preferences)
        )
        

    with open(file3) as f:
        lines = f.read()
        
        clustering_topics= list(
            csv.reader(lines.splitlines())
        )
    
        clustering_topics = list(
            map( lambda x: list(map( lambda y: eval(y), x)), clustering_topics)
        )
