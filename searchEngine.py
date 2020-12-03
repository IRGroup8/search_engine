from elasticsearch import Elasticsearch
import json
from nltk.corpus import wordnet
import nltk

# nltk.download('wordnet')


es = Elasticsearch(HOST="http://localhost", PORT=9200)
es = Elasticsearch()


# def docIndexing():
#     doc_id = 0
#     with open('output.json') as json_file:
#         for line in json_file:
#             doc = json.loads(line[0:len(line)-2])
#             es.index(index="news", doc_type="content", id=doc_id, body=doc)
#             doc_id = doc_id + 1
#
# docIndexing()


def get_wordnet(word):
    arr = []
    synset = wordnet.synsets(word)
    for syn in synset:
        for lemma in syn.lemmas():
            arr.append(lemma.name())
    return arr


def list_to_string(arr):
    str1 = ""
    for ele in arr:
        str1 += ele
        str1 += " OR "
    return str1[:-4]


def make_query(args):
    str_q = ""
    for arg in args:
        str_q += arg
        word_net = list_to_string(get_wordnet(arg))
        if word_net != "":
            str_q += " OR ("
            str_q += word_net
            str_q += ")"
        str_q += " AND "

    query = {"from": 0, "size": 500, "query": {"query_string": {"query": str_q[:-5]}}}
    return query


queries = [["USA"], ["iran"], ["vote"], ["USA", "trump"], ["facebook", "iran"],
           ["Prime", "Minister"], ["USA", "trump", "biden"], ["facebook", "iran", "president"],
           ["NYC", "Manhattan", "june"], ["USA", "trump", "biden", "November"],
           ["trump", "biden", "us", "president"], ["August", "people", "food", "health"],
           ["USA", "trump", "biden", "November", "Twitter"], ["facebook", "twitter", "social", "people", "world"],
           ["london", "article", "country", "story", "claims"]]

for query in queries:
    res = es.search(index="news", body=make_query(query))
    print("-----------------------------------------")
    for hit in res['hits']['hits']:
        print(hit["_source"])
