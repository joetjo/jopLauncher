import json

FILE = "biblio.json"

# 1 Load the json file
with open(FILE) as file:
    biblio = json.load(file, encoding='utf-8')

for livre in biblio:
    print("")
    print("[{}] {} - {}".format(livre["id"], livre["date"], livre["titre"]))
    print("Par: {}".format(livre["auteur"]))
    print("Résumé: {}".format(livre["description"]))
