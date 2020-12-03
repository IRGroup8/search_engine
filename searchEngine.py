from elasticsearch import Elasticsearch
import json

es = Elasticsearch(HOST="http://localhost", PORT=9200)
es = Elasticsearch()

def docIndexing():
    doc_id = 0
    with open('output.json') as json_file:
        for line in json_file:
            doc = json.loads(line[0:len(line)-2])
            es.index(index="news", doc_type="content", id=doc_id, body=doc)
            doc_id = doc_id + 1

docIndexing()



body={
    "from": 0,
    "size": 500,
    "query": {
        "match": {
            "content": "trump"
        }
    }
}

res = es.search(index="news", body=body)
print(res)