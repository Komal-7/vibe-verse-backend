import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Spotify client
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Output JSON file
output_file = "songs_data.json"

# Function to fetch track details and audio features from Spotify
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

# Function to fetch songs in batches and save them continuously
def fetch_and_store_songs(total_songs=500, batch_size=50):
    """Fetch songs in batches and save to JSON file continuously."""
    songs_data = []
    offset = 0

    # Load existing data if file exists
    try:
        with open(output_file, "r") as f:
            songs_data = json.load(f)
    except FileNotFoundError:
        pass

    while len(songs_data) < total_songs:
        try:
            # Fetch tracks
            results = sp.search(q="track", type="track", limit=batch_size, offset=offset)
            tracks = results["tracks"]["items"]

            # Fetch and process each track
            for track in tracks:
                if len(songs_data) >= total_songs:
                    break

                track_id = track["id"]
                try:
                    track_data = fetch_track_data(track_id)
                    songs_data.append(track_data)

                    # Save data after adding each track
                    with open(output_file, "w") as f:
                        json.dump(songs_data, f, indent=4)

                    print(f"Saved track: {track_data['title']} by {track_data['artist_name']}")
                except Exception as e:
                    print(f"Error fetching data for track {track_id}: {e}")

            offset += batch_size

            # Stop if no more tracks are available
            if len(tracks) < batch_size:
                print("No more tracks available.")
                break

        except Exception as e:
            print(f"Error fetching batch: {e}")
            break

# Run the fetching process
fetch_and_store_songs(total_songs=500)