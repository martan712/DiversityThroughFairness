# Does fairness foster diversity
### By Martan van der Straaten

This repository contains the full codebase used for the Bachelor Thesis of Martan van der Straaten. It is based on a repository provided by TREC, the repository is referenced via Github, and the original licence and README are still available under TREC_2022.md. 

## Guide
This Thesis was built on basis of a jupyter notebook, in this notebook we load all our documents and our queries. The main notebook used in this thesis is "Thesis copy.ipynb".

Under "Additional Notebooks" the notebook called "prepare and reduce memory" notebook describes how we built indexes from the very large json files that were provided by TREC. 

In the Library folder you can find any and all code that was written for this Thesis. E.g. reranking algorithms, evaluation metrics and the like.

To then get back to our main notebook, we first load this index and use pyserini with default parameters to get the top 200/500 documents per query. Code for this can be found in Libary/searcher.py. We check this with a basic example to see that this gives sensible results. The code for our various rerankers is also found in the Library folder, with each reranker being in the file corresponding to its name. The code for creating the LDA topic model over a set of documents is provided in Library/lda. Finally the evaluation metrics are in Library/evaluations.

With all this loaded into the notebook, we run over each query, computing the top 200/500 using BM25 score. We compute the topic information and clustering over each BM25 ranking per query. We then rerank these 200/500 documents using the 3 methods applied in this Thesis. We then obtain the relavancy documents and gender affiliation per document for each of these rerankings, through MetricInputs.py provided by TREC. Now, using the topic information, gender affiliation and the final rankings we compute the TREC score, NDCG and alpha-NDCG for each of our rerankers, per query. The resulting scores, and the gender distribution per query, are written to CSV files for further processing.

In the process_results notebook we look into these scores and the distribution. We visualise some results and compare methods.

In the statistical analysis notebook we compare two methods using a paired t_test.