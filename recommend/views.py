from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rdflib import Graph

# Load RDF Data into rdflib Graph
g = Graph()
g.parse("music_expert_django/songs_data.rdf", format="xml")  # Replace with your RDF file path and format

# Define filters
MOOD_FILTERS = {
    'happy': '?energy > 0.7 && ?valence > 0.7',
    'calm': '?energy < 0.4 && ?valence > 0.5 && ?acousticness > 0.6',
    'energetic': '?energy > 0.8 && ?danceability > 0.6',
    'sad': '?energy < 0.4 && ?valence < 0.4',
    'relaxed': '?energy < 0.5 && ?acousticness > 0.5 && ?loudness < -10',
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

@csrf_exempt
def recommend(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            filter_name = body.get('filter', '').lower()
            filter_type = body.get('filterType', 'popularity').lower()

            # Determine filter condition
            filter_condition = (
                MOOD_FILTERS.get(filter_name) or 
                ACTIVITY_FILTERS.get(filter_name) or 
                CUSTOM_COMBINATIONS_FILTERS.get(filter_name)
            )
            if not filter_condition:
                return JsonResponse({'error': 'Invalid filter selected'}, status=400)

            # Construct SPARQL Query
            sort_query = 'ORDER BY DESC(?popularity)' if filter_type == 'popularity' else 'ORDER BY RAND()'
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
                {sort_query}
            """

            # Execute Query
            results = g.query(sparql_query)
            recommendations = [
                {
                    'trackName': str(row.name),
                    'artistName': str(row.artistName),
                }
                for row in results
            ]

            return JsonResponse(recommendations, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
