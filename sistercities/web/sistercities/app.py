# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
import sistercities.web.sistercities.sister_graph as sister_graph
from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
import os.path, datetime

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = '86133838741634802826072472476'

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
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


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


@app.route('/')
@cache.cached(timeout=500)
def table():
    d = modification_date(app.open_resource('wikipedia.json').name)
    datajson = read_json_file(app.open_resource('wikipedia.json'))
    wikijson = read_json_file(app.open_resource('wikidata.json'))
    datasource = sister_graph.get(wikijson, datajson)

    return render_template('table.html', data=datasource, stats=d)


if __name__ == '__main__':
    # toolbar = DebugToolbarExtension(app)
    app.run()
