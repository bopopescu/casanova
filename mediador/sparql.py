from SPARQLWrapper import SPARQLWrapper
queryString = "SELECT * WHERE { ?s ?p ?o. }"
sparql = SPARQLWrapper("http://localhost:2020/sparql")
# add a default graph, though that can also be part of the query string
#sparql.addDefaultGraph("http://www.example.com/data.rdf")
sparql.setQuery(queryString)
try :
   ret = sparql.query()
   import pdb; pdb.set_trace()
   for binding in ret.next():
       print binding
except :
   pass
