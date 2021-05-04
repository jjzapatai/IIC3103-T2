from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os
from base64 import b64encode

from schema import *


# INIT
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postgresql-octagonal-02327')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
#Class/Model 
class Artist(db.Model):
  id = db.Column(db.String, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  age = db.Column(db.Integer)
  albums = db.Column(db.Integer)
  tracks = db.Column(db.String)
  self_url = db.Column(db.String)

  def __init__(self, name, age):
    self.name = name
    self.age = age
    self.id = b64encode(self.name.encode()).decode('utf-8')
    self.albums = 'http://localhost:5000/artists/'+self.id+'/albums'
    self.tracks = 'http://localhost:5000/artists/'+self.id+'/tracks'
    self.self_url = 'http://localhost:5000/artists/'+self.id

#Class/Model Album
class Album(db.Model):
  id = db.Column(db.String, primary_key=True)
  artist_id = db.Column(db.String, db.ForeignKey('artist.id'), nullable=False, unique=True)
  name = db.Column(db.String(100), unique=True)
  genre = db.Column(db.String)
  artist = db.Column(db.String)
  tracks = db.Column(db.String) #db.relationship("Track", backref="track", uselist=False)
  self_url = db.Column(db.String)

  def __init__(self, name, genre, artist_id):
    self.name = name
    self.id = b64encode(self.name.encode()).decode('utf-8')
    self.artist_id = artist_id
    self.genre = genre
    self.artist = 'http://localhost:5000/artists/'+self.id
    self.tracks = 'http://localhost:5000/albums/'+self.id+'/tracks'
    self.self_url = 'http://localhost:5000/albums/'+self.id
  #Class/Model Cancion
class Track(db.Model):
  id = db.Column(db.String, primary_key=True)
  album_id = db.Column(db.String, db.ForeignKey('album.id'), nullable=False)
  name = db.Column(db.String(100), unique=True)
  duration = db.Column(db.Float)
  times_played = db.Column(db.Integer)
  artist = db.Column(db.String)
  album = db.Column(db.String)
  self_url = db.Column(db.String)

  def __init__(self, name, duration, album_id):
    self.name = name
    self.album_id = album_id
    self.id = b64encode(self.name.encode()).decode('utf-8')
    self.duration = duration
    self.times_played = 0
    self.artist = 'http://localhost:5000/artists/'+self.id
    self.album = 'http://localhost:5000/albums/'+self.id
    self.self_url = 'http://localhost:5000/tracks/'+self.id



## hacer python   ->  from app import db  -> db.create_all()  (y se crea la base de datos)
##########################################     ARTISTS     ##########################################     
#CREATE AN ARTIST
@app.route('/artists', methods=['POST'])
def add_artist():
  name = request.json['name']
  age = request.json['age']
  print(name)
 #########   ARREGLARTODOESTOOO    ########
  name_artist = Artist.query.get('U1RJQ0tZIEZJTkdFUlM=')
  age_artist = Artist.query.get(age)
  new_artist = Artist(name, age)

  db.session.add(new_artist)
  db.session.commit()

  return artist_schema.jsonify(new_artist), 201

 
  #return jsonify({"message": "invalid parameters"}), 400

## errores: artista ya existe: 409. 
## errores: input invalido: 400. 
  


## GET ALL ARTISTS
@app.route('/artists', methods=['GET'])
def get_artists():
  all_artists = Artist.query.all()
  if  all_artists is None:
    return jsonify({"No hay Artistas ingresados": "404"})
  else: 
    result = artists_schema.dump(all_artists), 200
    return jsonify(result)

## GET SINGLE ARTIST
@app.route('/artists/<id>', methods=['GET'])
def get_artist(id):
  artist = Artist.query.get(id)
  if artist is None:
    return jsonify({'message': 'Artist does not exists'}), 404

  else:
    return artist_schema.jsonify(artist), 200

## GET ALBUMS OF ARTIST
# @app.route('/artists/<artist_id>/albums', methods=['GET'])
# def get_albums_of_artist(artist_id):

#   results = []
#   all_artists = Artist.query.filter(Artist.artist_id == artist_id)
#   # if  not artist in artists:
#   #   return jsonify({"No existe el artista": "404"}), 404
#   result = albums_schema.dump(all_artists)
#   print(result)
#   # for album in result:
#   #   print(artist_id)
#   #   if album['artist_id'] == 'Q0hFVCBGQUtFUg==':
#   #     results.append(0)
#   # for key, value in result:
#   #   print(key, value)
#   print(len(result))
#   return albums_schema.jsonify(result)


#DELETE ARTIST
@app.route('/artists/<id>', methods=['DELETE'])
def delete_artist(id):
  artist = Artist.query.get(id)            ## metodos de sqlalchemy: query, dump, data
  
  if artist is None:
    return jsonify({'message': 'Artist does not exists'}), 404

  else:
    db.session.delete(artist)
    db.session.commit()
    return artist_schema.jsonify(artist), 204

##########################################     ALBUMS     ##########################################     
#CREATE AN ALBUM
@app.route('/artists/<artist_id>/albums', methods=['POST'])
def add_album(artist_id):
  artist = artist_id
  name = request.json['name']
  genre = request.json['genre']

  new_album = Album(name, genre, artist)

  db.session.add(new_album)
  db.session.commit()

  return album_schema.jsonify(new_album), 201
  ## errores: album ya existe: 409. 
  ## errores: input invalido: 400. 
  ## errores: artista no existe: 422. 

## GET ALL ALBUMS
@app.route('/albums', methods=['GET'])
def get_albums():
  all_albums = Album.query.all()
  result = albums_schema.dump(all_albums)
  print("###########################")
  print(result)
  if all_albums is None:
    return jsonify({'message': 'No albums yet'}), 404
  else:
    return jsonify(result)

## GET SINGLE ALBUM
@app.route('/albums/<id>', methods=['GET'])
def get_album(id):
  album = Album.query.get(id)
  if album is None:
    return jsonify({'message': 'Album no encontrado'}), 404
  else:
    return album_schema.jsonify(album), 200

# ## GET TRACKS OF ALBUM
# @app.route('/albums/<album_id>/tracks', methods=['GET'])
# def get_tracks_of_album(album_id):
#   album = Artist.query.get(album_id) 
#   albums = 

#   if  artist is None:
#     abort(404)
#     return jsonify({"error": "error 404"})

#   else:
#     return artist_schema.jsonify(artist)

#DELETE ALBUM
@app.route('/albums/<id>', methods=['DELETE'])
def delete_album(id):
  album = Album.query.get(id)
  db.session.delete(album)
  db.session.commit()
  if album is None:
    return jsonify({'message': 'Album no encontrado'}), 404

  else:
    return album_schema.jsonify(album), 204


##########################################     TRACKS     ##########################################     
#CREATE A TRACK
@app.route('/albums/<album_id>/tracks', methods=['POST'])
def add_track(album_id):
  album = album_id
  name = request.json['name']
  duration = request.json['duration']

  new_track = Track(name, duration, album)

  db.session.add(new_track)
  db.session.commit()

  return album_schema.jsonify(new_track), 201
  
  ## errores: track ya existe: 409. 
  ## errores: input invalido: 400. 
  ## errores: album no existe: 422. 

## GET ALL TRACKS
@app.route('/tracks', methods=['GET'])
def get_tracks():
  all_tracks = Track.query.all()
  result = tracks_schema.dump(all_tracks)
  if all_tracks is None:
    return jsonify({'message': 'No hay canciones'}), 404
  else:
    return jsonify(result), 200

## GET SINGLE TRACK
@app.route('/tracks/<id>', methods=['GET'])
def get_track(id):
  track = Track.query.get(id)
  if track is None:
    return jsonify({'message': 'Canción no encontrada'}), 404
  else:
    return track_schema.jsonify(track), 200

#DELETE TRACK
@app.route('/tracks/<id>', methods=['DELETE'])
def delete_track(id):
  track = Track.query.get(id)
  db.session.delete(track)
  db.session.commit()
  if track is None:
    return jsonify({'message': 'Canción no encontrada'}), 404

  else:
    return album_schema.jsonify(track), 204

# #PLAY A TRACK
# @app.route('/tracks/<track_id>/play', methods=['PUT'])
# def play_tack(track_id):
#   album = album_id
#   new_track = Track(name, duration, album)

#   db.session.add(new_track)
#   db.session.commit()

#   return album_schema.jsonify(new_track), 201



# Run Server
if __name__ == '__main__':
  app.run(debug=True)
