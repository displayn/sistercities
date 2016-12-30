import networkx as nx
from networkx.readwrite import json_graph
import json

def read_json_file(filename):
    # from http://stackoverflow.com/a/34665365
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)



if __name__ == '__main__':
    read_json_file("wikidata.json")
