import re
import gensim
import gensim
import nltk
from nltk.corpus import stopwords
import spacy
import gensim.corpora as corpora
from pyserini.search.lucene import LuceneSearcher
import json
import pandas as pd

# Download NLTK stopwords
nltk.download('stopwords')
stop_words = stopwords.words('english')

datapath = "."

def get_clustering(result, queries, ranking_index = 0, searcher = LuceneSearcher(f"{datapath}/data/indexes/indexes/lucene-index"), n_clusters = 10):
    def preprocess_text(text):
        text = re.sub('\s+', ' ', text)  # Remove extra spaces
        text = re.sub('\S*@\S*\s?', '', text)  # Remove emails
        text = re.sub('\'', '', text)  # Remove apostrophes
        text = re.sub('[^a-zA-Z]', ' ', text)  # Remove non-alphabet characters
        text = text.lower()  # Convert to lowercase
        return text
    def tokenize(text):
        tokens = gensim.utils.simple_preprocess(text, deacc=True)
        tokens = [token for token in tokens if token not in stop_words]
        return tokens

    def lemmatize(tokens):
        doc = nlp(" ".join(tokens))
        return [token.lemma_ for token in doc]
    
    documents = list(
        map(
            lambda x: json.loads(searcher.doc(x.docid).raw())['contents'], result
        )
    )

    data = pd.DataFrame(documents, columns=["text"])
    data['cleaned_text'] = data["text"].apply(preprocess_text)

    # Load spaCy model
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    data['tokens'] = data['cleaned_text'].apply(tokenize)
    data['lemmas'] = data['tokens'].apply(lemmatize)

    # Create dictionary and corpus
    id2word = corpora.Dictionary(data['lemmas'])
    texts = data['lemmas']
    corpus = [id2word.doc2bow(text) for text in texts]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics= n_clusters, 
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)

    rankedClusters = list(
    map(lambda d: 
        d[[y for (x,y) in d].index(max([y for (x,y) in d]))][0], lda_model.get_document_topics(corpus))
    )

    lda_model.print_topics()
    
    x = corpora.Dictionary(lemmatize(tokenize(preprocess_text(
        ' '.join(queries.iloc[ranking_index]["keywords"])
    ))))
    
    cluster_preferences = lda_model[ id2word.doc2bow(x)]

    return rankedClusters, cluster_preferences, lda_model.get_document_topics(corpus, minimum_probability=0)