import networkx as nx
from networkx.readwrite import json_graph
import json

def read_json_file(filename):
    # from http://stackoverflow.com/a/34665365
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)



if __name__ == '__main__':
    wikipedia = read_json_file("wikipedia.json")
    wikidata = read_json_file('wikidata.json')

    #stats
    print(nx.number_of_nodes(wikipedia))
    print(nx.number_of_nodes(wikidata))

    root_nodes = nx.get_node_attributes(wikipedia, 'group')
    wikidata_root_nodes = nx.get_node_attributes(wikidata, 'group')
    #assert (len(root_nodes) is len(wikidata_root_nodes)), 'Error: Graph root size should be the same!'


    url = nx.get_node_attributes(wikipedia, 'url')
    #print(root_nodes.keys())

    for c in root_nodes.keys():
        print('the city '+c+ ' '+url.get(c))
        #load all result root nodes
        wg_neighbors = nx.all_neighbors(wikipedia,c)
        wd_neighbors =nx.all_neighbors(wikidata,c)

        pedia = set(wg_neighbors)
        data = set(wd_neighbors)

        merge = set(pedia).intersection(data)
        print("intersection:", end='')
        print(merge)
        print('missing on wikipedia: ', end='')
        wikipedia_missing = set(data) - set(pedia)
        print(wikipedia_missing)
        print('missing on wikidata: ', end='')
        wikidata_missing = set(pedia) - set(data)
        print(wikidata_missing)

        for sister in wg_neighbors:
            print(sister+ ' '+url.get(sister))
        print('as sister cities')

        print(' ')

