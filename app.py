from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
data_movie = pd.read_csv('movieindex.csv')
print(data_movie)

matrix_movie = pd.read_csv('sorted_lists.csv', header=None)
print(matrix_movie)

data_tv = pd.read_csv('tvindex.csv')
print(data_tv)

matrix_tv = pd.read_csv('sorted_lists_tv.csv', header=None)
print(matrix_tv)

def recommend1(tv_id):
    if int(tv_id) not in data_tv['id'].values:
        return []
    index = data_tv[data_tv['id'] == int(tv_id)].index[0]
    lii = matrix_tv.iloc[index]
   
    recommendations = []
    for idx in lii:
        recommendations.append(
            {
                'id': str(data_tv.iloc[idx]['id']),
                'name': data_tv.iloc[idx]['name'],
                'poster_path': data_tv.iloc[idx]['poster_path']
            }
        )
    
    return recommendations

def recommend2(movie_id):

    if int(movie_id) not in data_movie['id'].values:
        return []

    index = data_movie[data_movie['id'] == int(movie_id)].index[0]
    lii = matrix_movie.iloc[index]
   
    recommendations = []
    for idx in lii:
        recommendations.append(
            {
                'id': str(data_movie.iloc[idx]['id']),
                'title': data_movie.iloc[idx]['title'],
                'poster_path': data_movie.iloc[idx]['poster_path']
            }
        )
    
    return recommendations

@app.route('/recommend/movie', methods=['POST'])
def recommend_movie():
    request_data_movie = request.json
    movie_id = request_data_movie.get('id')
    recommendations = recommend2(movie_id)
    return jsonify({
        'recommendations': recommendations
    })

@app.route('/recommend/tv', methods=['POST'])
def recommend_tv():
    request_data_tv = request.json
    tv_id = request_data_tv.get('id')
    recommendations = recommend1(tv_id)
    return jsonify({
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
