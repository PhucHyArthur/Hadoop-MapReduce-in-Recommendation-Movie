#!/usr/bin/env python3
import sys
from math import log
from collections import defaultdict

# Initialize variables
tag_movies = defaultdict(list)  # key: tagId, value: list of (movieId, relevance)
total_movies = set()  # Set of all movies

# Input format: tagId \t movieId:relevance
for line in sys.stdin:
    tag_id, data = line.strip().split('\t')
    movie_id, relevance = data.split(':')
    relevance = float(relevance)
    tag_movies[tag_id].append((movie_id, relevance))
    total_movies.add(movie_id)

# Total number of movies
total_movies_count = len(total_movies)

# Compute TF-IDF
for tag_id, movie_data in tag_movies.items():
    idf = log(total_movies_count / len(movie_data))  # Inverse Document Frequency
    for movie_id, relevance in movie_data:
        tf_idf = relevance * idf  # TF-IDF score
        # Output: movieId \t tagId:tf_idf
        print(f"{movie_id}\t{tag_id}:{tf_idf}")
