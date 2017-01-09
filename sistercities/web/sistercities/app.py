# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
import sistercities.web.sistercities.sister_graph as sister_graph
from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '86133838741634802826072472476'

cache = Cache(app,config={'CACHE_TYPE': 'simple'})
from networkx.readwrite import json_graph
import json

def read_json_file(filename: object) -> object:
    # from http://stackoverflow.com/a/34665365
    """

    :type filename: object
    """
    with open(filename.name) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


@app.route('/')
@cache.cached(timeout=500)
def table():
    datajson = read_json_file(app.open_resource('wikipedia.json'))
    wikijson = read_json_file(app.open_resource('wikidata.json'))
    datasource = sister_graph.get(wikijson, datajson)

    return render_template('table.html', data=datasource)


if __name__ == '__main__':
    #toolbar = DebugToolbarExtension(app)
    app.run()
