from flask import Flask, request, jsonify
from flask_cors import CORS
from rdflib import Graph
from queries import CUSTOM_QUERIES

app = Flask(__name__)
CORS(app)

# Load RDF data into an RDFLib Graph
rdf_file_path = "vibe-verse-backend/songs_data.rdf"
graph = Graph()
graph.parse(rdf_file_path, format="xml")

# Define filters
MOOD_FILTERS = {
    "happy": "?energy > 0.7 && ?valence > 0.7",
    "calm": "?energy < 0.4 && ?valence > 0.5 && ?acousticness > 0.6",
    "energetic": "?energy > 0.8 && ?danceability > 0.6",
    "relaxed": "?energy < 0.5 && ?acousticness > 0.5 && ?loudness < -10",
    "romantic": "?tempo < 100 && ?valence > 0.5 && ?acousticness > 0.4",  
    "melancholic": "?energy < 0.3 && ?valence < 0.4",
}

ACTIVITY_FILTERS = {
    'workout': '?energy > 0.8 && ?tempo > 120 && ?danceability > 0.6',
    'study': '?energy < 0.5 && ?instrumentalness > 0.5 && ?speechiness < 0.3',
    'party': '?danceability > 0.8 && ?energy > 0.7 && ?loudness > -5',
    'meditation': "?energy < 0.4 && ?acousticness > 0.6 && ?valence > 0.4",  
    'driving': '?energy > 0.6 && ?tempo > 100 && ?tempo < 140 && ?valence > 0.5',
    'relaxing': '?energy < 0.4 && ?valence > 0.5',
}

CUSTOM_COMBINATIONS_FILTERS = {
    'bright energy for driving': '?energy > 0.5 && ?valence > 0.6 && ?tempo >= 100',
    'melancholic with acoustic feel': '?energy < 0.3 && ?acousticness > 0.8',
    'light effort during workout': '?energy < 0.5 && ?danceability > 0.6',
    'relaxed ride for driving': '?energy < 0.5 && ?tempo <= 100',
}

@app.route('/api/recommend', methods=['POST'])
def recommend_music():
    data = request.json
    filter_key = data.get("filter", "").lower().strip()
    print("Received Filter Key:", filter_key)
    filter_type = data.get("filterType", "popularity").lower()

    all_filters = {**MOOD_FILTERS, **ACTIVITY_FILTERS, **CUSTOM_COMBINATIONS_FILTERS}
    filter_condition = all_filters.get(filter_key)
    if not filter_condition:
        return jsonify({"error": f"Invalid filter selected: {filter_key}"}), 400

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
        if len(recommendations) == 0:
            return jsonify({"error": "Not enough recommendations for the selected filter"}), 404

        return jsonify({"query": sparql_query.strip(), "recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": "Failed to fetch recommendations", "details": str(e)}), 500
    
@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    query = data.get("query", "").strip().lower()
    
    if not query:
        return jsonify({"error": "Search query cannot be empty"}), 400

    sparql_query = f"""
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT ?name ?artistName
        WHERE {{
            ?track a rdf:Track .
            ?track rdf:name ?name .
            ?track rdf:performedBy ?artist .
            ?artist rdf:name ?artistName .
            FILTER (CONTAINS(LCASE(?name), "{query}") || CONTAINS(LCASE(?artistName), "{query}"))
        }}
    """
    try:
        results = graph.query(sparql_query)
        search_results = [
            {"trackName": str(row.name), "artistName": str(row.artistName)}
            for row in results
        ]
        if not search_results:
            return jsonify({"message": "No results found for your search query."}), 200
        return jsonify({"query": sparql_query.strip(), "recommendations": search_results})
    except Exception as e:
        return jsonify({"error": "Failed to execute search", "details": str(e)}), 500

    
@app.route('/api/surprise', methods=['GET'])
def surprise_me():
    sparql_query = """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT ?name ?artistName
        WHERE {
            ?track a rdf:Track .
            ?track rdf:name ?name .
            ?track rdf:performedBy ?artist .
            ?artist rdf:name ?artistName .
        }
        ORDER BY RAND()
        LIMIT 25
    """
    try:
        results = graph.query(sparql_query)
        recommendations = [
            {"trackName": str(row.name), "artistName": str(row.artistName)}
            for row in results
        ]
        return jsonify({"query": sparql_query.strip(), "recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": "Failed to fetch random songs", "details": str(e)}), 500

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
        results = graph.query(sparql_query)
        if query_key == "get all artist names":
            response = [{"artistName": str(row.artistName)} for row in results]
        elif query_key == "all albums of coldplay":
            response = [{"albumName": str(row.albumName)} for row in results]
        elif query_key == "get count and avg popularity of taylor swift's tracks for each album":
            response = [{"albumName": str(row.albumName), "count": str(row.songCount),  "averagePopularity": str(row.averagePopularity)} for row in results]
        elif query_key == "rewind to the 2000s" :
            response = [{"trackName": str(row.trackName),"artistName": str(row.artistName),"releaseDate": str(row.releaseDate),"popularity": str(row.popularity)} for row in results]
        elif query_key == "same energy as song calm down" :
            response = [{"similarTrackName": str(row.similarTrackName),"artistName": str(row.artistName),"energy": str(row.energy)} for row in results]
        elif query_key == "gradual tempo increase" :
            response = [{"trackName": str(row.trackName),"tempoRange": str(row.tempoRange),"tempo": str(row.tempo)} for row in results]
        elif query_key == "transition my mood" :
            response = [{"trackName": str(row.trackName),"energy": str(row.energy),"valence": str(row.valence),"valenceRange": str(row.valenceRange)} for row in results]
        else:
            response = []
        returnValue = {
            "query": sparql_query.strip(),  # Include the current query
            "recommendations": response,  # Include the recommendations
        }
        return jsonify(returnValue)
    except Exception as e:
        return jsonify({"error": "Failed to execute custom query", "details": str(e)}), 500
    
if __name__ == '__main__':
    app.run(port=5000)