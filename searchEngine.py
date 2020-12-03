from elasticsearch import Elasticsearch

es = Elasticsearch(HOST="http://localhost", PORT=9200)
es = Elasticsearch()


doc_1 = {"sentence":"Hack COVID-19 is amazing!"}
doc_2 = {"sentence":"Hack-Quarantine is stunning!"}

es.index(index="english", doc_type="sentences", id=1, body=doc_1)
es.index(index="english", doc_type="sentences", id=2, body=doc_2)


body = {
    "from":0,
    "size":2,
    "query": {
        "bool": {
            "must_not": {
                "match": {
                    "sentence":"COVID-19"
                }
            },
            "should": {
                "match": {
                    "sentence": "Hack"
                }
            }
        }
    }
}
res = es.search(index="english", body=body)


print(res)