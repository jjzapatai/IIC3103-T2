# #UPDATE A ARTIST
# @app.route('/artists/<id>', methods=['PUT'])
# def update_artist(id):
#   artist = Artist.query.get(id)

#   id = request.json['id']
#   name = request.json['name']
#   age = request.json['age']
#   albums = request.json['albums']
#   tracks = request.json['tracks']
#   self_url = request.json['self_url']

#   artist.id = id
#   artist.name = name
#   artist.age = age
#   artist.albums = albums
#   artist.tracks = tracks
#   artist.self_url = self_url

#   db.session.commit()

#   return artist_schema.jsonify(artist)