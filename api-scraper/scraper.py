import spotipy
spotify = spotipy.Spotify()
results = spotify.search(q='track:' + '', limit=50, offset=0, type='track')
tracks = results['tracks']
items = tracks['items']
i = 0
songs = {}
artistGenres = {'DummyID': 'DummyGenre'}
for track in items:
    artists = ""
    for artist in track['artists']:
        artists += artist['name'] + " && "
    artists = artists.rstrip(" && ")
    if (!artistGenres.has_key(track['artists'][0]['id'])):
        artistResult = spotify.artist(track['artists'][0]['uri'])
        artistGenres[track['artists'][0]['id']] = ""
        for genre in artistResult['genres']:
            artistGenres[track['artists'][0]['id']] += genre + ", "
        artistGenres[track['artists'][0]['id']] = artistGenres[track['artists'][0]['id']].rstrip(", ")
    songs[i] = {track['name'], artists, track['album']['name'], track['popularity'], track['duration_ms'], artistGenres[track['artists'][0]['id']], track['external_urls']['spotify']}
    i += 1
print songs[0]
