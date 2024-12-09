
# Define the custom queries
CUSTOM_QUERIES = {
    "get all artist names": """
        PREFIX rdf: <http://www.semanticweb.org/musicontology#>
        SELECT DISTINCT ?artistName ?trackName
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
    """
}



