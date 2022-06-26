import pandas as pd
import numpy as np
from gensim.test.utils import datapath, get_tmpfile
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix, save_npz

# Transform each word in overview int vector using glove word embedding, then
# compute a vector representation for the whole overview as a the mean vector of
# all its words. Use those vectors for similarity between overviews

def get_sentence_vector(sntce, model):
    w_list = sntce.lower().split()
    n_words = len(w_list)
    mean_vector = np.zeros(model.vector_size)
    for w in w_list:
        try:
            mean_vector += model.get_vector(w)
        except:
            # word not found so do not take it into accoutn for average
            n_words -= 1
    return mean_vector/n_words


if __name__ == '__main__':
    # get pre-trained word embeddings
    glove_fn = 'glove.6B.50d'
    word2vec_glove_file = get_tmpfile(f"{glove_fn}.word2vec.txt")
    glove_path = "C:\javier\personal_projects\ml\movie-recommender\movie_recommender_system\data"
    glove_file = datapath(f'{glove_path}\{glove_fn}.txt')
    glove2word2vec(glove_file, word2vec_glove_file)
    model = KeyedVectors.load_word2vec_format(word2vec_glove_file)

    # get filtered movies
    movies = pd.read_csv('src/movies_filtered.csv')

    # removing stop-words and mapping sentence to vector using the glove model
    ov_vecs = movies['overview'].apply(lambda x: remove_stopwords(x.lower()))
    ov_vecs = ov_vecs.apply(lambda x: get_sentence_vector(x, model=model))

    # computing cosine similarity metric
    n_words = len(ov_vecs)
    smat = np.zeros((n_words, model.vector_size))
    for i, wvec in enumerate(ov_vecs):
        smat[i, :] = wvec
    ov_metric = cosine_similarity(smat)

    filename = 'src/metrics/overview_cos_similarity'
    save_npz(filename, csr_matrix(ov_metric))