
# Define the custom queries
CUSTOM_QUERIES = {
    "gradual tempo increase": """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT ?tempoRange (SAMPLE(?selectedTrack) AS ?trackName) ?tempo
        WHERE {   
            ?track a rdf:Track ;
                    rdf:name ?selectedTrack ;
                    rdf:energy ?energy ;
                    rdf:tempo ?tempo .
                    
            BIND(FLOOR(?tempo / 5) * 5 AS ?tempoRange)
            
            FILTER(?tempo >= 100 && ?energy > 0.7)
        }
        GROUP BY ?tempoRange
        ORDER BY ?tempoRange
    """,
    "transition my mood": """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT ?valenceRange (SAMPLE(?selectedTrack) AS ?trackName) ?valence ?energy
        WHERE {
            ?track a rdf:Track ;
                    rdf:name ?selectedTrack ;
                    rdf:energy ?energy ;
                    rdf:valence ?valence .
            BIND(FLOOR(?valence * 10) / 10 AS ?valenceRange)
        }
        GROUP BY ?valenceRange
        ORDER BY ?valenceRange
    """,
    "get all artist names": """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT DISTINCT ?artistName
        WHERE {
            ?artist a rdf:Artist .
            ?artist rdf:name ?artistName .
        }
    """,
    "all albums of coldplay": """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT DISTINCT ?albumName
        WHERE {
            
            ?track a rdf:Track ;
                    rdf:name ?trackname ;
                    rdf:performedBy ?artist ;
                    rdf:partOfAlbum ?album .
            ?album rdf:name ?albumName .
            ?artist rdf:name "Coldplay" .
        }
    """,
    "get count and avg popularity of taylor swift's tracks for each album" : """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT ?albumName (COUNT(?track) AS ?songCount) (AVG(?popularity) AS ?averagePopularity)
        WHERE {
            ?track a rdf:Track ;
                    rdf:partOfAlbum ?album ;
                    rdf:popularity ?popularity ;
                    rdf:performedBy ?artist .
            ?album rdf:name ?albumName .
            ?artist rdf:name "Taylor Swift" .
        }
        GROUP BY ?albumName
        ORDER BY DESC(?songCount)
    """,
    "rewind to the 2000s" : """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT ?trackName ?artistName ?releaseDate ?popularity
        WHERE {
            ?track a rdf:Track ;
                    rdf:name ?trackName ;
                    rdf:releaseDate ?releaseDate ;
                    rdf:popularity ?popularity ;
                    rdf:performedBy ?artist .
            ?artist rdf:name ?artistName .
            FILTER(?releaseDate >= "2000-01-01" && ?releaseDate < "2010-01-01")
        }
        ORDER BY DESC(?popularity)
    """,
    "same energy as song calm down" : """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT DISTINCT ?similarTrackName ?artistName ?energy
        WHERE {
            ?calmDownTrack a rdf:Track ;
                    rdf:name "Calm Down (with Selena Gomez)" ;
                    rdf:energy ?calmDownEnergy .

            ?track a rdf:Track ;
                    rdf:name ?similarTrackName ;
                    rdf:energy ?energy ;
                    rdf:performedBy ?artist .
            ?artist rdf:name ?artistName .

            FILTER(ABS(?energy - ?calmDownEnergy) < 0.05)
            FILTER(?similarTrackName != "Calm Down (with Selena Gomez)")
        }
        ORDER BY ?similarTrackName
    """
}