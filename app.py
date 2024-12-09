from flask import Flask, request, jsonify
from flask_cors import CORS
from rdflib import Graph
from queries import CUSTOM_QUERIES
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load RDF data into an RDFLib Graph
rdf_file_path = "vibe-verse-backend/songs_data.rdf"  # Path to your RDF file
graph = Graph()
graph.parse(rdf_file_path, format="xml")  # Adjust format if not XML

# Define filters
MOOD_FILTERS = {
    "happy": "?energy > 0.7 && ?valence > 0.7",
    "calm": "?energy < 0.4 && ?valence > 0.5 && ?acousticness > 0.6",
    "energetic": "?energy > 0.8 && ?danceability > 0.6",
    "sad": "?energy < 0.4 && ?valence < 0.4",
    "relaxed": "?energy < 0.5 && ?acousticness > 0.5 && ?loudness < -10",
}
ACTIVITY_FILTERS = {
    'workout': '?energy > 0.8 && ?tempo > 120 && ?danceability > 0.6',
    'study': '?energy < 0.5 && ?instrumentalness > 0.5 && ?speechiness < 0.3',
    'party': '?danceability > 0.8 && ?energy > 0.7 && ?loudness > -5',
    'meditation': '?energy < 0.3 && ?acousticness > 0.8 && ?valence > 0.5',
    'driving': '?energy > 0.6 && ?tempo > 100 && ?tempo < 140 && ?valence > 0.5',
}
# Custom combinations filters
CUSTOM_COMBINATIONS_FILTERS = {
    'intense focus for study': '?energy > 0.6 && ?valence > 0.7 && ?instrumentalness > 0.5',
    'peaceful joy in meditation': '?energy < 0.3 && ?valence > 0.8 && ?acousticness > 0.8',
    'bright energy for driving': '?energy > 0.5 && ?valence > 0.6 && ?tempo >= 100',
    'deep calm in meditation practice': '?energy < 0.2 && ?acousticness > 0.9',
    'high energy for workout sessions': '?energy > 0.8 && ?tempo > 120 && ?danceability > 0.6',
    'vibrant energy for party time': '?danceability > 0.8 && ?energy > 0.7',
    'light effort during workout': '?energy < 0.5 && ?danceability > 0.6',
    'calm study time': '?energy < 0.4 && ?instrumentalness > 0.6',
    'relaxed ride for driving through nature': '?energy < 0.5 && ?tempo <= 100',
}

@app.route('/api/recommend', methods=['POST'])
def recommend_music():
    data = request.json
    filter_key = data.get("filter", "").lower().strip()
    filter_type = data.get("filterType", "popularity").lower()
    filter_condition = (
                MOOD_FILTERS.get(filter_key) or 
                ACTIVITY_FILTERS.get(filter_key) or 
                CUSTOM_COMBINATIONS_FILTERS.get(filter_key)
            )
    if not filter_condition:
        return jsonify({"error": "Invalid filter selected"}), 400

    sort_clause = (
        "ORDER BY DESC(?popularity)" if filter_type == "popularity" else "ORDER BY RAND()"
    )

    sparql_query = f"""
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
                SELECT ?name ?artistName
                WHERE {{
                    ?track a rdf:Track .
                    ?track rdf:name ?name .
                    ?track rdf:performedBy ?artist .
                    ?artist rdf:name ?artistName .
                    ?track rdf:popularity ?popularity .

                    ?track rdf:energy ?energy .
                    ?track rdf:valence ?valence .
                    ?track rdf:danceability ?danceability .
                    ?track rdf:acousticness ?acousticness .
                    ?track rdf:loudness ?loudness .
                    ?track rdf:tempo ?tempo .
                    ?track rdf:instrumentalness ?instrumentalness .
                    ?track rdf:speechiness ?speechiness .

                    FILTER ({filter_condition})
                }}
        {sort_clause}
    """
    try:
        results = graph.query(sparql_query)
        recommendations = [
            {"trackName": str(row.name), "artistName": str(row.artistName)}
            for row in results
        ]
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": "Failed to fetch recommendations"}), 500

def get_custom_query_sparql(query_key):
    return CUSTOM_QUERIES.get(query_key)

@app.route('/api/custom-query', methods=['POST'])
def execute_custom_query():
    data = request.json
    query_key = data.get("filter", "").lower().strip()
    sparql_query = get_custom_query_sparql(query_key)
    if not sparql_query:
        return jsonify({"error": "Invalid custom query selected"}), 400

    try:
        print(sparql_query)
        results = graph.query(sparql_query)
        print(results)
        if query_key == "get all artist names":
            response = [{"artistName": str(row.artistName)} for row in results]
        elif query_key == "all albums of coldplay":
            response = [{"albumName": str(row.albumName)} for row in results]
        elif query_key == "get count and avg popularity of taylor swift's tracks for each album":
            response = [{"albumName": str(row.albumName), "count": str(row.songCount),  "averagePopularity": str(row.averagePopularity)} for row in results]
        else:
            response = []
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": "Failed to execute custom query", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
