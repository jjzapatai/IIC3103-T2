from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

from app import ma

# Artist Schema
class ArtistSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'age', 'albums', 'tracks', 'self_url')

# Album Schema
class AlbumSchema(ma.Schema):
  class Meta:
    fields = ('id', 'artist_id', 'name', 'genre', 'artist', 'tracks', 'self_url')

# Track Schema
class TrackSchema(ma.Schema):
  class Meta:
    fields = ('id', 'album_id', 'name', 'duration', 'times_played', 'artist', 'album', 'self_url')

#init schema
artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)

track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)