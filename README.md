In this project, 

## Step 1 :

Fetched song data from Spotify api using scripts - `fetch500ToJson.py , fetchPlaylist.py` and stored it as json `songs_data.json`. Fetched randomly and from different public playlists.

## Step 2 :
Converted the json data to rdf format `songs_data.rdf` using - `jsonToRdf.py`

## Step 3 : 
Loaded the rdf data in the rdflib and used SparQL to query the song data in `app.py`

## Ontologies used :
The script uses the following ontology terminologies from the namespace http://www.semanticweb.org/musicontology#:

```bash
MO.Track: Represents a track or song.
MO.Artist: Represents an artist.
MO.Album: Represents an album.
MO.name: The name of a track, artist, or album.
MO.popularity: Popularity of the track (integer).
MO.acousticness: Acousticness score of the track (float).
MO.danceability: Danceability score of the track (float).
MO.duration_ms: Duration of the track in milliseconds (integer).
MO.energy: Energy score of the track (float).
MO.instrumentalness: Instrumentalness score of the track (float).
MO.key: Musical key of the track (integer).
MO.liveness: Liveness score of the track (float).
MO.loudness: Loudness level of the track (float).
MO.mode: Mode of the track (integer; 1 = major, 0 = minor).
MO.speechiness: Speechiness score of the track (float).
MO.tempo: Tempo of the track in BPM (float).
MO.time_signature: Time signature of the track (integer).
MO.track_href: Spotify track URL (URI).
MO.valence: Valence score of the track (float).
MO.releaseDate: Release date of the track (date).
MO.performedBy: Relates a track to its artist.
MO.partOfAlbum: Relates a track to its album.
```


Install dependencies listed in `requirements.txt`

Run `python app.py`
