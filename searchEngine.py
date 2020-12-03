from elasticsearch import Elasticsearch
import json
from nltk.corpus import wordnet
import nltk
# nltk.download('wordnet')


synset = wordnet.synsets("Travel")
print(synset[0].lemmas()[0].name())


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


query15={
    "from": 0,
    "size": 500,
    "query": {
        "query_string": {
            "query": "london AND article AND country AND story AND claims"
        }
    }
}

res = es.search(index="news", body=query15)

for hit in res['hits']['hits']:
    print(hit["_source"])