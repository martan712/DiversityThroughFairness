import numpy as np
import scipy 
from tqdm.auto import tqdm
tqdm.pandas(leave=False)

from Library.fairness import get_fairness

def MMR(ranked_list_inp, comp_function, lamb = 0.5):
    ranked_list = ranked_list_inp[:]
    output_list = [ranked_list[0]]
    ranked_list.pop(0)
        
    # compute an optimum with lambda between ranking score and similarity (comp_fucntion)

    while len(output_list) < 100:
        intermediate_list = [
            lamb*item.score - ((1- lamb) * comp_function(item, output_list))
            for item in ranked_list]

        index = intermediate_list.index(max(intermediate_list))
        output_list.append( 
            ranked_list.pop(index)
        ) 
    return output_list

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def MMR_gender(ranked_list_inp, lamb = 0.5):

    TOTAL_RERANK = 100
    ranked_list = ranked_list_inp[:]
    fairness_df = get_fairness(ranked_list)
    print(f"Missing fairness info for {len(ranked_list)-len(fairness_df)} values!")
    output_list = [ranked_list.pop(0)]

    scores = list(NormalizeData([doc.score for doc in ranked_list]))

    def compare_d1_d2_fairness(d, curr, fairness_df):
        docs = [x.docid for x in curr]
        before = fairness_df.loc[ fairness_df.index.isin([eval(x) for x in docs])].mean()
        after = fairness_df.loc[ fairness_df.index.isin([eval(x) for x in docs+[d]])].mean()
        
        return scipy.spatial.distance.jensenshannon( before, after)  

    # compute an optimum with lambda between ranking score and similarity (comp_fucntion)
    with tqdm(total=TOTAL_RERANK, position=0) as pbar:
        while len(output_list) < TOTAL_RERANK:
            pbar.update(1)
            intermediate_list = [
                lamb*scores[i] + ((1- lamb) * compare_d1_d2_fairness(item.docid, output_list, fairness_df))
                for i, item in enumerate(ranked_list)]
            
            index = intermediate_list.index(max(intermediate_list))
            optimum = ranked_list.pop(index)
            scores.pop(index)
            output_list.append( 
                optimum
            ) 
            
    return output_list