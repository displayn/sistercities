# -*- coding: utf-8 -*-
import datetime
import json
import os
import os.path

from flask import Flask
from flask import render_template
from flask_cache import Cache

import sistercities.web.sistercities.sister_graph as sister_graph

app = Flask(__name__)
#app.debug = True
#TEMPLATES_AUTO_RELOAD = True
app.config['SECRET_KEY'] = os.urandom(24)
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app, config={'CACHE_TYPE': 'simple'})




def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


@app.route('/')
@cache.cached(timeout=500)
def table():
    d = modification_date(app.open_resource('wikipedia.json').name)
    datajson = sister_graph.read_json_file(app.open_resource('wikipedia.json'))
    wikijson = sister_graph.read_json_file(app.open_resource('wikidata.json'))
    datasource = sister_graph.get(wikijson, datajson)

    return render_template('table.html', data=datasource, stats=d)


if __name__ == '__main__':
    app.run()
