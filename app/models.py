# -*- coding: utf-8 -*-

import json
from app import db
from sqlalchemy.orm import relationship, backref

movie_actor = db.Table('movie_actor',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)

movie_location = db.Table('movie_location',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'))
)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String(36))
    title = db.Column(db.String(255))
    imdb_url = db.Column(db.String(255))
    year = db.Column(db.String(4))
    locations = db.relationship('Location', secondary=movie_location,
                backref=db.backref('movies', lazy='dynamic'))
    facts = db.Column(db.Text(1000))
    production_company = db.Column(db.String(255))
    distributor = db.Column(db.String(255))
    director = db.Column(db.String(255))
    writer = db.Column(db.String(255))
    actors = db.relationship('Actor', secondary=movie_actor,
                backref=db.backref('movies', lazy='dynamic'))

    def load_from_api(self, data):
        pass

    def __repr__(self):
        print '<Movie %s (%s)>' % (self.title, self.year)

    def serialize(self):
        output = {}
        output['id'] = self.id
        output['title'] = str(self.title)
        output['year'] = str(self.year)
        output['locations_count'] = len(self.locations)
        output['locations'] = [str(location.address.encode('utf-8')) for location in self.locations]
        output['actors'] = [str(actor.name) for actor in self.actors]
        output['director'] = str(self.director)
        return output


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name):
        self.name = name


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))

    def __init__(self, movie_id, address):
        self.movie_id = movie_id
        self.address = address
