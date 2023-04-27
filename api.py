from flask import Flask, request, jsonify
from utils import ArabicIndexer
from methods import preprocess
import pandas as pd

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

indexer = ArabicIndexer.load("indexer/indexer.pkl")

data = pd.read_csv("data.csv")

def fetch_document_data(doc_id):
    
    document_row = data[data["docno"] == doc_id]

    if document_row.empty:
        return None

    document_data = {
        "title": document_row["titles"].values[0],
        "raw_texts": document_row["raw_texts"].values[0]
    }

    return document_data


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    top_n = request.args.get("top_n", 10)
    
    try:
        top_n = int(top_n)
    except ValueError:
        top_n = 10

    query = preprocess(query)
    
    results = indexer.search(query, top_n)
    
    # look for the file diroctory with doc_id in results
    files = [data[data["docno"] == doc_id]["files"].values[0] for doc_id, _ in results]
    
    # look for the title of the document with doc_id in results
    titles = [data[data["docno"] == doc_id]["titles"].values[0] for doc_id, _ in results]

    descriptions = [data[data["docno"] == doc_id]["description"].values[0] for doc_id, _ in results]
    
    result_docs = [{"doc_id": doc_id, "score": score, "file": file, "titles": title,"description":description} for (doc_id, score), file, title ,description in zip(results, files, titles,descriptions)]
    response = {"results": result_docs}
    return jsonify(response)

@app.route("/document", methods=["GET"])
def get_document():
    doc_id = request.args.get("doc_id", None)

    if doc_id is None:
        return jsonify({"error": "doc_id is required"}), 400

    # Fetch the document data from your data source using the doc_id
    document_data = fetch_document_data(doc_id)

    if document_data is None:
        return jsonify({"error": "Document not found"}), 404

    return jsonify(document_data)
