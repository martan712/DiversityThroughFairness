from MetricInputs import *

def get_fairness(ranking):
    ranking_docids = [doc.docid for doc in ranking]
    resulting_fairness = gender_align.loc[ gender_align.index.isin([eval(x) for x in ranking_docids])]

    return resulting_fairness

def get_fairness2(ranking_docids):
    resulting_fairness = gender_align.loc[ gender_align.index.isin([eval(x) for x in ranking_docids])]

    return resulting_fairness