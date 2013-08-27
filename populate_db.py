import json
import urllib2
import sys
from app import db
from app.models import Movie, Location, Actor


def get_imdb_url(title, year, director):
    print '====================================='
    imdb_url = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s' % title.replace(' ', '+')
    print "URL: " + imdb_url
    try:
        imdb_id = None
        imdb_data = json.loads(urllib2.urlopen(imdb_url).read())
        for movie in imdb_data.get('title_exact', []):
            #print movie
            #print "Title: %s" % title
            #print movie.get('title').lower() == title.lower()
            #print "Year: %s" % year
            #print year in movie.get('title_description')
            #print "Director: %s" % director
            #print director in movie.get('title_description').lower()
            if movie.get('title').lower() == title.lower() and \
               year in movie.get('title_description') and \
               director.lower() in movie.get('title_description').lower():
                imdb_id = movie.get('id')
                break
            else:
                print "NOT FOUND"
                print "TITLE: %s - %s" % (title.lower(), movie.get('title').lower())
                print "YEAR: %s - %s" % (year.lower(), movie.get('title').lower())
                print "DIRECTOR: %s - %s" % (director.lower(), movie.get('title').lower())

        if not imdb_id:
            return None
        else:
            return 'http://www.imdb.com/title/%s' % imdb_id
    except:
        raise
        return None


# Create tables
db.create_all()

data_url = 'https://data.sfgov.org/api/views/yitu-d5am/rows.json?accessType=DOWNLOAD'
data_url = 'http://0.0.0.0:8000/data.json'
data = json.loads(urllib2.urlopen(data_url).read())

"""
The dump of the data from DataSF is not properly formatted for reading
so we need to identify the column order first and then parse the lists
with the actual data
"""
columns = data.get('meta').get('view').get('columns')
data_name_mapping = {
    'id': 'api_id',
    'Title': 'title',
    'Release Year': 'year',
    'Locations': 'locations',
    'Fun Facts': 'facts',
    'Production Company': 'production_company',
    'Distributor': 'distributor',
    'Director': 'director',
    'Writer': 'writer',
    'Actor 1': 'actor_1',
    'Actor 2': 'actor_2',
    'Actor 3': 'actor_3'
}

column_pos = {}
pos = 0
for column in columns:
    name = column.get('name')
    if name:
        mapped = data_name_mapping.get(column.get('name'))
        column_pos[mapped] = pos
    pos += 1


for movie_data in data.get('data'):
    movie_api_id = movie_data[column_pos.get('api_id')]
    title = movie_data[column_pos.get('title')]
    year = movie_data[column_pos.get('year')]
    director = movie_data[column_pos.get('director')]
    movie = Movie.query.filter(Movie.title == title,
                               Movie.year == year,
                               Movie.director == director).first()
    if not movie:
        movie = Movie()
        movie.api_id = movie_data[column_pos.get('api_id')]
        sys.stdout.write('\rNEW Movie %s' % movie.api_id)
        movie.title = movie_data[column_pos.get('title')]
        movie.year = movie_data[column_pos.get('year')]
        movie.director = movie_data[column_pos.get('director')]
        # Set actors
        actors = [
            movie_data[column_pos.get('actor_1')],
            movie_data[column_pos.get('actor_2')],
            movie_data[column_pos.get('actor_3')]
        ]
        for actor_name in [a for a in actors if a]:
            actor = Actor.query.filter(Actor.name == actor_name).first()
            if not actor:
                actor = Actor(actor_name)
            movie.actors.append(actor)
        # Set IMDB url
        movie.imdb_url = get_imdb_url(movie.title, movie.year, movie.director)
        db.session.add(movie)
    else:
        sys.stdout.write('\rOLD Movie %s' % movie.api_id)

    location = Location(movie.id, movie_data[column_pos.get('locations')])
    movie.locations.append(location)
    db.session.commit()
sys.stdout.write('\r\n')
