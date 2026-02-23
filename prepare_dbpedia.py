from rdflib import Graph
import os

print("Loading DBpedia... (may take few minutes)")

g = Graph()
g.parse("dataset/dbpedia_2016-04.owl")

knowledge = []

for s, p, o in list(g)[:5000]:   # limit for laptop
    knowledge.append(f"{s} {p} {o}")

os.makedirs("dataset", exist_ok=True)

with open("dataset/dbpedia_knowledge.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(knowledge))

print("✅ DBpedia converted → dataset/dbpedia_knowledge.txt")