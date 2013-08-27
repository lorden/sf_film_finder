# -*- coding: utf-8 -*-

import json
from models import Movie, Actor, Location
from app import app, db
from flask import make_response, render_template, request


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movies')
def search():
    q = request.values.get('q')
    results = []
    # Query movies titles
    movies = Movie.query.filter(Movie.title.ilike('%' + q + '%'))
    for movie in movies:
        results.append(movie.serialize())

    # Query actors
    movies = Movie.query.join(Actor.movies).filter(Actor.name.ilike('%' + q + '%'))
    for movie in movies:
        results.append(movie.serialize())

    # Query directors
    movies = Movie.query.filter(Movie.director.ilike('%' + q + '%'))
    for movie in movies:
        results.append(movie.serialize())

    # Query locations
    movies = Movie.query.join(Location.movies).filter(Location.address.ilike('%' + q + '%'))
    for movie in movies:
        results.append(movie.serialize())

    res = make_response(json.dumps(results))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/movies/<movie_id>')
def movies(movie_id):
    movie = Movie.query.get(movie_id).serialize()
    res = make_response(json.dumps(movie))
    res.mimetype = 'application/json'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
