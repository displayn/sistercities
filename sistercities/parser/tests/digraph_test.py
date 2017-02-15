import networkx as nx
from networkx.readwrite import json_graph
import json

'''
digraph_test is a small script that shows the difference between
non directed an directed graphs in the scope of cities
'''


def write_graph(data: object, filename: object) -> object:
    fd = open(filename, 'w')
    fd.write(str(data))
    fd.close()


def directed_graph_method():
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    print("DI GRAPH IS HOLDING:")
    print(str(G.number_of_nodes()),' nodes')

    G.add_edge('Q42', 'Q64')

    print("Q42 neighbors")
    print(G.neighbors('Q42'))


    write_graph(json.dumps(json_graph.node_link_data(G)), 'di_test.json')


def non_directed_graph_method():
    F = nx.Graph()
    F.add_nodes_from(nodes)
    F.add_edges_from(edges)

    print("NON DI GRAPH IS HOLDING:")
    print(str(F.number_of_nodes()), 'nodes')

    F.add_edge('Q42', 'Q64')

    print("Q42 neighbors")
    print(F.neighbors('Q42'))

    write_graph(json.dumps(json_graph.node_link_data(F)), 'non_di_test.json')

if __name__ == '__main__':
    # nodes we want to add to the graph
    nodes = {'Q64', 'Q42', 'Q32'}
    #edges that are connected
    edges = {('Q64', 'Q32'), ('Q64', 'Q42')}
    non_directed_graph_method()
    print('-----------')
    directed_graph_method()
