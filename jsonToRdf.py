import json
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from rdflib.namespace import XSD

# File paths
json_file = "songs_data.json"
rdf_output_file = "songs_data.rdf"

# Define RDF namespaces
MO = Namespace("http://www.semanticweb.org/musicontology#")

# Initialize RDF graph
graph = Graph()

# Load JSON data
with open(json_file, "r") as f:
    songs_data = json.load(f)

# Add songs data to RDF graph
for song in songs_data:
    song_uri = URIRef(f"_:track_{song['id']}")
    artist_uri = URIRef(f"_:artist_{song['id']}")
    album_uri = URIRef(f"_:album_{song['id']}")

    # Add track details
    graph.add((song_uri, RDF.type, MO.Track))
    graph.add((song_uri, MO.name, Literal(song["title"])))
    graph.add((song_uri, MO.popularity, Literal(song["popularity"], datatype=XSD.integer)))
    graph.add((song_uri, MO.acousticness, Literal(song["acousticness"], datatype=XSD.float)))
    graph.add((song_uri, MO.danceability, Literal(song["danceability"], datatype=XSD.float)))
    graph.add((song_uri, MO.duration_ms, Literal(song["duration_ms"], datatype=XSD.integer)))
    graph.add((song_uri, MO.energy, Literal(song["energy"], datatype=XSD.float)))
    graph.add((song_uri, MO.instrumentalness, Literal(song["instrumentalness"], datatype=XSD.float)))
    graph.add((song_uri, MO.key, Literal(song["key"], datatype=XSD.integer)))
    graph.add((song_uri, MO.liveness, Literal(song["liveness"], datatype=XSD.float)))
    graph.add((song_uri, MO.loudness, Literal(song["loudness"], datatype=XSD.float)))
    graph.add((song_uri, MO.mode, Literal(song["mode"], datatype=XSD.integer)))
    graph.add((song_uri, MO.speechiness, Literal(song["speechiness"], datatype=XSD.float)))
    graph.add((song_uri, MO.tempo, Literal(song["tempo"], datatype=XSD.float)))
    graph.add((song_uri, MO.time_signature, Literal(song["time_signature"], datatype=XSD.integer)))
    graph.add((song_uri, MO.valence, Literal(song["valence"], datatype=XSD.float)))
    graph.add((song_uri, MO.releaseDate, Literal(song["release_date"])))

    # Add artist details
    graph.add((artist_uri, RDF.type, MO.Artist))
    graph.add((artist_uri, MO.name, Literal(song["artist_name"])))

    # Add album details
    graph.add((album_uri, RDF.type, MO.Album))
    graph.add((album_uri, MO.name, Literal(song["album_name"])))

    # Relate track to artist and album
    graph.add((song_uri, MO.performedBy, artist_uri))
    graph.add((song_uri, MO.partOfAlbum, album_uri))

# Serialize RDF graph to a file
graph.serialize(destination=rdf_output_file, format="xml")

print(f"RDF data has been saved to {rdf_output_file}")
