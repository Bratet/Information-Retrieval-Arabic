from flask import Flask, render_template, url_for, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils import *
from methods import *
import pandas as pd


app = Flask(__name__)


@app.route('/', methods=['GET'])
def search():
    query = request.args.get ('query')
    indexer = ArabicIndexer().load('indexer/indexer.pkl')
    query = preprocess(query)
    results = indexer.search(query)
    return jsonify({'result': results})


if __name__ == "__main__":
    app.run(debug=True)