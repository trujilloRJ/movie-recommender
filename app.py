from flask import Flask, request, render_template
from src.get_recomendations import fetch_recommendations, load_data

# development server
# app = Flask(__name__)

# production server
app = Flask(__name__, static_folder="frontend/build", static_url_path='/', template_folder='frontend/build')

# loading data
movies, combined_metric = load_data()

@app.route("/")
def hello():
    return render_template('index.html')
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/get_recs')
def get_recommendations():
    film_name = request.args.get('film_name', default='The Matrix')
    print(film_name)
    try:
        recs = fetch_recommendations(movies, film_name, combined_metric)
        recs = recs.to_dict('records')
    except Exception as e:
        recs = []
    return {'recommendations': recs}


@app.route('/get_possible_movies')
def get_movies():
    try:
        search_term = request.args.get('search_term', default='The Matrix')
        possible_movies = list(movies['original_title'][movies['original_title'].str.contains(search_term, case=False)])[:10]
    except Exception:
        possible_movies = []
    return {'possible_movies': possible_movies}

if __name__ == '__main__':
    app.run()