from elasticsearch import Elasticsearch

es = Elasticsearch(HOST="http://localhost", PORT=9200)
es = Elasticsearch()

def docIndexing():
    doc_id = 0
    with open('output.json') as json_file:
        for line in json_file:
            doc = json.loads(line[0:len(line)-2])
            es.index(index="news", doc_type="content", id=doc_id, body=doc)
            doc_id = doc_id + 1
            print(doc)

docIndexing()


# doc_1 = {"sentence":"Hack COVID-19 is amazing!"}
# doc_2 = {"sentence":"Hack-Quarantine is stunning!"}
#
# es.index(index="english", doc_type="sentences", id=1, body=doc_1)
# es.index(index="english", doc_type="sentences", id=2, body=doc_2)
#
#
#
# body = {
#     "from":0,
#     "size":2,
#     "query": {
#         "bool": {
#             "must_not": {
#                 "match": {
#                     "sentence":"COVID-19"
#                 }
#             },
#             "should": {
#                 "match": {
#                     "sentence": "Hack"
#                 }
#             }
#         }
#     }
# }
# res = es.search(index="english", body=bo
# print(res)