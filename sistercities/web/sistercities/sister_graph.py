# -*- coding: utf-8 -*-
import networkx as nx
from networkx.readwrite import json_graph
import json
import collections


def read_json_file(filename: object) -> object:
    # from http://stackoverflow.com/a/34665365
    with open(filename) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


def city_build(name_list, qid_list) -> object:
    object_list = []
    for e in qid_list:
        x = collections.OrderedDict()
        x = [e, name_list[e]]
        object_list.append(x)
    return object_list


def get(w, d) -> object:
    wikipedia = w
    wikidata = d

    root_nodes = nx.get_node_attributes(wikipedia, 'group')
    wikidata_root_nodes = nx.get_node_attributes(wikidata, 'group')
    assert (len(root_nodes) == len(wikidata_root_nodes)), 'Error: Graph root size should be the same!'

    url_wiki = nx.get_node_attributes(wikipedia, 'url')
    url_data = nx.get_node_attributes(wikidata, 'url')
    city_list = []
    for c in root_nodes.keys():
        # print('the city ' + c + ' ' + url.get(c))
        # load all result root nodes
        wg_neighbors = nx.all_neighbors(wikipedia, c)
        wd_neighbors = nx.all_neighbors(wikidata, c)

        pedia = set(wg_neighbors)
        data = set(wd_neighbors)

        intersection = set(pedia).intersection(data)
        wikipedia_missing = set(data) - set(pedia)
        wikidata_missing = set(pedia) - set(data)

        city_dict = {'qid': c,
                     'url': url_wiki[c],
                     'miss_wikipedia': city_build(url_data, wikipedia_missing),
                     'intersection': city_build(url_wiki, intersection),
                     'data_cities': city_build(url_wiki, wikidata_missing)
                     }
        city_list.append(city_dict)
        #sort all elemnts to url, to get a sorted list
        city_list = sorted(city_list, key=lambda x: x['url'])
    return city_list


#get(read_json_file('wikipedia.json'), read_json_file('wikidata.json'))
