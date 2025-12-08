import os
import json
import csv
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

DATA_FOLDER = "html_docs"
INDEX_FILE = "index.json"

# Load index
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    index = json.load(f)

doc_ids = list(index.keys())
documents = [" ".join(index[d].keys()) for d in doc_ids]

vocab = {term: i for i, term in enumerate(set().union(*[d.keys() for d in index.values()]))}
vectorizer = TfidfVectorizer(vocabulary=vocab)
tfidf_matrix = vectorizer.fit_transform(documents).toarray()

# Function to process queries
def process_queries(query_list, top_k=3):
    output_rows = []
    for query_id, query_text in query_list:
        query_vec = vectorizer.transform([query_text]).toarray()
        scores = cosine_similarity(query_vec, tfidf_matrix)[0]
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        rank = 1
        for idx in ranked_indices:
            output_rows.append({
                "query_id": query_id,
                "rank": rank,
                "document_id": doc_ids[idx]
            })
            rank += 1
    return output_rows

# Flask endpoint
@app.route("/search", methods=["POST"])
def search():
    if "file" not in request.files:
        return jsonify({"error": "No CSV file uploaded"}), 400

    file = request.files["file"]
    queries = []
    reader = csv.DictReader(file.stream.read().decode("utf-8").splitlines())
    for row in reader:
        queries.append((row["query_id"], row["query"]))

    results = process_queries(queries, top_k=3)

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["query_id", "rank", "document_id"])
        writer.writeheader()
        writer.writerows(results)

    return jsonify({"message": "results.csv created"})

if __name__ == "__main__":
    app.run(debug=True)
