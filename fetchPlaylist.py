import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# JSON file to store song data
output_file = "songs_data.json"

# Function to fetch track details and audio features from Spotify API
def fetch_track_data(track_id):
    """Fetch track details and audio features from Spotify API."""
    track = sp.track(track_id)
    features = sp.audio_features(track_id)[0]

    # Extract required data
    track_data = {
        "id": track["id"],
        "title": track["name"],
        "artist_name": track["artists"][0]["name"],
        "album_name": track["album"]["name"],
        "release_date": track["album"]["release_date"],
        "popularity": track["popularity"],
        "acousticness": features["acousticness"],
        "danceability": features["danceability"],
        "duration_ms": features["duration_ms"],
        "energy": features["energy"],
        "instrumentalness": features["instrumentalness"],
        "key": features["key"],
        "liveness": features["liveness"],
        "loudness": features["loudness"],
        "mode": features["mode"],
        "speechiness": features["speechiness"],
        "tempo": features["tempo"],
        "time_signature": features["time_signature"],
        "track_href": features["track_href"],
        "valence": features["valence"],
    }
    return track_data

# Function to fetch all songs from a playlist using its ID
def fetch_playlist_songs_by_id(playlist_id):
    """Fetch all songs from the given Spotify playlist ID."""
    playlist_tracks = sp.playlist_tracks(playlist_id)
    songs = []
    for item in playlist_tracks["items"]:
        track = item["track"]
        if track:
            songs.append(track["id"])
    return songs

# Function to add new songs to JSON file
def add_new_songs_to_json(playlist_id):
    """Add new songs from playlist to JSON file."""
    # Load existing data
    try:
        with open(output_file, "r") as f:
            songs_data = json.load(f)
            existing_ids = {song["id"] for song in songs_data}
    except FileNotFoundError:
        songs_data = []
        existing_ids = set()

    # Fetch all songs from the playlist
    playlist_songs = fetch_playlist_songs_by_id(playlist_id)

    # Add only new songs
    for track_id in playlist_songs:
        if track_id not in existing_ids:
            try:
                track_data = fetch_track_data(track_id)
                songs_data.append(track_data)
                existing_ids.add(track_id)

                # Save after adding each new song
                with open(output_file, "w") as f:
                    json.dump(songs_data, f, indent=4)
                print(f"Added song: {track_data['title']} by {track_data['artist_name']}")
            except Exception as e:
                print(f"Error fetching track {track_id}: {e}")

# Run the script
playlist_id = "5l771HfZDqlBsDFQzO0431"  # Replace with your playlist ID
add_new_songs_to_json(playlist_id)

# playlist ids used :
# 37i9dQZF1DX18jTM2l2fJY
# 56r5qRUv3jSxADdmBkhcz7
# 5GhQiRkGuqzpWZSE7OU4Se
# 2fmTTbBkXi8pewbUvG3CeZ
# 37i9dQZF1DWVRSukIED0e9
# 37i9dQZF1DX4o1oenSJRJd
# 5l771HfZDqlBsDFQzO0431
# 01pNIDYGqmeawppy32wr3D
# 37i9dQZF1DX48TTZL62Yht
# 2wwz6rOtTzHvQEbqmBB79e
# 0VvcLAmjej4BIZxfO5J8Rd
# 5iwkYfnHAGMEFLiHFFGnP4