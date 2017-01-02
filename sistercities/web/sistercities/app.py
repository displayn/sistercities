# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from sistercities.web.sistercities import sister_graph
app = Flask(__name__)


@app.route('/')
def table():

    return render_template('table.html', name = sister_graph.get())

if __name__ == '__main__':
    app.run()
