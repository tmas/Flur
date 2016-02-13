import spotipy
spotify = spotipy.Spotify()
results = spotify.search(q='track:' + '', limit=1, offset=0, type='track')
tracks = results['tracks']
items = tracks['items']
i = 0
songs = {}
for track in items:
    artists = ""
    for artist in track['artists']:
        artists += artist['name'] + " && "
    artists = artists.rstrip(" && ")
    songs[i] = {track['name'], artists, track['album']['name'], track['popularity'], track['duration_ms'], track['external_urls']['spotify']}
    i += 1
print songs[0]
