import numpy as np
import pandas as pd
from scipy.sparse import load_npz, save_npz, csr_matrix

def fetch_recommendations(movies_df, film_name, metric):
    film_id = movies_df[movies_df['original_title'] == film_name].index[0]
    rec_ids = metric[film_id, :]
    
    return movies_df.loc[rec_ids, :]

def put_genre_as_list(genre):
    try:
        return genre.split(' ')
    except:
        return []

def load_data():
    movies = pd.read_csv('src/movies_filtered.csv', index_col=None)
    movies['genres'] = movies['genres'].apply(put_genre_as_list)
    combined_metric = np.load('src/metrics/reduced_metric.npy')
    return movies, combined_metric

if __name__ == '__main__':
    # loading data
    movies, combined_metric = load_data()

    # get recommnedations
    film_name = 'Misery'
    recs = fetch_recommendations(movies, film_name, combined_metric)
    print(list(recs.loc[:, 'original_title']))
    recs = recs.to_dict('records')
