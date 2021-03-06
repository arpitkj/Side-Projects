# -*- coding: utf-8 -*-
"""Movie Recommender.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/arpitkj/Movie-recommender/blob/main/Movie_Recommender.ipynb
"""

#importing libraries
import numpy as np
import pandas as pd

#reading files from Movielens dataset
data = pd.io.parsers.read_csv('/content/drive/MyDrive/movie recommender/ml-1m/ratings.dat', names=['user_id', 'movie_id', 'rating', 'time'], engine='python', delimiter='::')

movie_data = pd.io.parsers.read_csv('/content/drive/MyDrive/movie recommender/ml-1m/movies.dat',names=['movie_id', 'title', 'genre'],engine='python', delimiter='::')

data.head()

movie_data.head()

#Creating the ratings matrix with rows as movies and columns as users
ratings_mat = np.ndarray(shape=(np.max(data.movie_id.values), np.max(data.user_id.values)),dtype=np.uint8)

ratings_mat[data.movie_id.values-1, data.user_id.values-1] = data.rating.values

#normalising matrix
normalised_mat = ratings_mat - np.asarray([(np.mean(ratings_mat, 1))]).T

#computing svd
A = normalised_mat.T / np.sqrt(ratings_mat.shape[0] - 1)
U, S, V = np.linalg.svd(A)

#calculating cosine similarity and returning top n results
def top_cosine_similarity(data, movie_id, top_n=10):
    index = movie_id - 1 # Movie id starts from 1
    movie_row = data[index, :]
    magnitude = np.sqrt(np.einsum('ij, ij -> i', data, data))
    similarity = np.dot(movie_row, data.T) / (magnitude[index] * magnitude)
    sort_indexes = np.argsort(-similarity)
    return sort_indexes[:top_n]

# Helper function to print top N similar movies
def print_similar_movies(movie_data, movie_id, top_indexes):
    print('Recommendations for {0}: \n'.format(
    movie_data[movie_data.movie_id == movie_id].title.values[0]))
    for id in top_indexes + 1:
        print(movie_data[movie_data.movie_id == id].title.values[0])

#Select  principal components to represent the movies, a movie_id to find recommendations and print the top_n results.
k = 50
movie_id = 2 # Grab an id from movies.dat
top_n = 10

sliced = V.T[:, :k] # representative data
indexes = top_cosine_similarity(sliced, movie_id, top_n)
print_similar_movies(movie_data, movie_id, indexes)