# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
import sistercities.web.sistercities.sister_graph as sister_graph

app = Flask(__name__)
from networkx.readwrite import json_graph
import json
import os


def read_json_file(filename: object) -> object:
    # from http://stackoverflow.com/a/34665365
    """

    :type filename: object
    """
    with open(filename.name) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


@app.route('/')
def table():
    datajson = read_json_file(app.open_resource('wikipedia.json'))
    wikijson = read_json_file(app.open_resource('wikidata.json'))

    datasource = sister_graph.get(wikijson, datajson)

    return render_template('table.html', data=datasource)


if __name__ == '__main__':
    app.run(debug=True)
