from elasticsearch import Elasticsearch
import json
from nltk.corpus import wordnet
import nltk

# nltk.download('wordnet')


es = Elasticsearch(HOST="http://localhost", PORT=9200)
es = Elasticsearch()


def docIndexing():
    doc_id = 0
    with open('output.json') as json_file:
        for line in json_file:
            doc = json.loads(line[0:len(line) - 2])
            es.index(index="new", doc_type="content", id=doc_id, body=doc)
            doc_id = doc_id + 1


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


# make query without wordnet
def make_query_without(args):
    str_q = ""
    for arg in args:
        str_q += arg
        str_q += " AND "
    query = {"from": 0, "size": 10, "query": {"query_string": {"query": str_q[:-5]}}}
    return query


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

# A sample of the query which was made: {'from': 0, 'size': 500, 'query': {'query_string': {'query': 'london OR (
# London OR Greater_London OR British_capital OR capital_of_the_United_Kingdom OR London OR Jack_London OR
# John_Griffith_Chaney) AND article OR (article OR article OR article OR clause OR article OR article) AND country OR
# (state OR nation OR country OR land OR commonwealth OR res_publica OR body_politic OR country OR state OR land OR
# nation OR land OR country OR country OR rural_area OR area OR country) AND story OR (narrative OR narration OR
# story OR tale OR story OR floor OR level OR storey OR story OR history OR account OR chronicle OR story OR report
# OR news_report OR story OR account OR write_up OR fib OR story OR tale OR tarradiddle OR taradiddle) AND claims OR
# (claim OR claim OR claim OR claim OR title OR title OR claim OR call OR claim OR claim OR claim OR lay_claim OR
# arrogate OR claim OR claim OR take OR claim OR take OR exact)'}}}

# ------------------------MAMAD OUTPUT-------------------
with open('newOutput.json', 'w') as file:
    for query in queries:
        res = es.search(index="new", body=make_query(query))
        file.write("Query for %s :\n" % str(query))
        for hit in res['hits']['hits']:
            hit["_source"]['score'] = hit["_score"]
            json.dump(hit["_source"], file)
            file.write('\n')
        file.write('\n\n')
