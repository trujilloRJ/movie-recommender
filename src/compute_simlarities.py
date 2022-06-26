import pandas as pd
import numpy as np
import os 
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.test.utils import get_tmpfile
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec


def get_country_name(pc):
    pc = ast.literal_eval(pc)
    if not isinstance(pc, list):
        return ''
    return '' if len(pc) == 0 else pc[0]['name']


def extract_cast(cast):
    credit_list = ast.literal_eval(cast)
    return ' '.join([''.join(act['name'].lower().split(' ')) for act in credit_list])


def extract_director(crew):
    for cm in ast.literal_eval(crew):
        if cm['job'] == 'Director':
            return ''.join(cm['name'].lower().split(' '))
    return ''


def load_and_filter_movies(min_votes=25):
    # loading movies
    movies = pd.read_csv('data/movies_metadata.csv')

    # cleaning data
    movies.drop_duplicates(subset=['original_title'], inplace=True)
    movies.dropna(subset=['overview', 'vote_average', 'genres', 'production_countries', 'release_date'], inplace=True)

    # filtering by languages
    languages = ['en', 'es', 'fr', 'it', 'de']
    movies = movies[movies['original_language'].isin(languages)]

    # get recent movies
    from_year = 1970
    movies['release_year'] = movies['release_date'].str[:4]
    movies = movies[movies['release_year'].astype(float) > from_year]

    # filtering for (to estimate with a reduced dataset)
    movies['production_countries'] = movies['production_countries'].apply(get_country_name)
    mean_vote = movies['vote_average'].mean()
    most_voted = \
        (movies['vote_count'] >= min_votes) & \
        (movies['vote_average'] >= mean_vote - 1.0)
    movies = movies[most_voted]

    # formating genre
    movies['genres'] = movies['genres'].apply(lambda genre: ' '.join([g['name'] for g in ast.literal_eval(genre)]).lower())
    return movies.reset_index(drop=True)


def add_credits_to_movies(movies, director_factor=2):
    # getting credits
    m_credits = pd.read_csv('data/credits.csv')

    # keeping credits for the selected films
    movies['id'] = movies['id'].astype('int64')
    m_credits = pd.merge(m_credits, movies, on='id', how='inner')

    # we need to get the actors name from the cast and the director name from the crew
    m_credits['cast'] = m_credits['cast'].apply(extract_cast)
    m_credits = m_credits[m_credits['cast'] != ''].reset_index(drop=True)
    m_credits['director'] = m_credits['crew'].apply(extract_director)
    m_credits = m_credits[m_credits['director'] != ''].reset_index(drop=True)

    # adding the director to the cast to have the complete cast
    m_credits['whole_cast'] = m_credits['cast'] + director_factor*(' ' + m_credits['director'])
    return m_credits


def get_cossim_metric(doc, stop_words='english'):
    # tokenizing doc
    cv = CountVectorizer(stop_words=stop_words, token_pattern=r'\b[^\d\W]+\b')
    x = cv.fit_transform(doc)
    metric = cosine_similarity(x.toarray())
    return metric


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


def get_ov_cossim(movies):
    # get pre-trained word embeddings
    glove_fn = 'glove.6B.50d'
    word2vec_glove_file = get_tmpfile(f"{glove_fn}.word2vec.txt")
    glove_file = os.path.abspath(f"data/{glove_fn}.txt")
    glove2word2vec(glove_file, word2vec_glove_file)
    model = KeyedVectors.load_word2vec_format(word2vec_glove_file)

    # removing stop-words and mapping sentence to vector using the glove model
    ov_vecs = movies['overview'].apply(lambda x: remove_stopwords(x.lower()))
    ov_vecs = ov_vecs.apply(lambda x: get_sentence_vector(x, model=model))

    # computing cosine similarity metric
    n_words = len(ov_vecs)
    smat = np.zeros((n_words, model.vector_size))
    for i, wvec in enumerate(ov_vecs):
        smat[i, :] = wvec
    return cosine_similarity(smat)


if __name__ == "__main__":
    # parameters
    min_votes = 25
    director_factor = 2
    gen_stop_words = ['the', 'movie', 'production', 'productions', 'film']

    # fetching and processing data
    movies = load_and_filter_movies(min_votes)
    movies = add_credits_to_movies(movies, director_factor)
    
    # saving filtered movies
    keep_columns = ['original_title', 'overview', 'genres', 'release_year', 'vote_average', 'imdb_id']
    print(f'Total number of movies: {movies.shape[0]}')
    movies[keep_columns].to_csv('src/movies_filtered.csv')

    # getting cosine similarity metrics for genre and cast
    print('Getting genre similarity...')
    genre_metric = get_cossim_metric(movies['genres'], stop_words=gen_stop_words)
    print('Getting casting similarity...')
    cast_metric = get_cossim_metric(movies['whole_cast'])

    # getting cosine similarity metrics for overview (precomputed with word embedding)
    print('Getting overview similarity...')
    # overview_metric = load_npz('src/metrics/overview_cos_similarity.npz').toarray()
    overview_metric = get_ov_cossim(movies)

    # getting combined metric, compressing it and save
    gen_w, ov_w, cast_w = 0.05, 0.15, 0.80
    combined_metric = gen_w*genre_metric + ov_w*overview_metric + cast_w*cast_metric
    for i in range(combined_metric.shape[0]):
        combined_metric[i][i] = -1
    reduced_metric = np.flip(np.argsort(combined_metric, axis=1), axis=1)[:, :10]

    np.save('src/metrics/reduced_metric.npy', reduced_metric)

