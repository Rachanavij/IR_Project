import json
import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load stored index components
print("Loading index files...")

with open("doc_ids.json", "r", encoding="utf-8") as f:
    doc_ids = json.load(f)

vectorizer = joblib.load("vectorizer.pkl")
tfidf_matrix = joblib.load("tfidf_matrix.pkl")

print(f"Loaded {len(doc_ids)} documents.")

# Process Queries
queries_file = "queries.csv"
results_file = "results.csv"

queries = []
with open(queries_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        queries.append(row["query"])

print(f"Loaded {len(queries)} queries.")

# Compute Similarities
print("Processing queries...")

results = []
for q_id, query in enumerate(queries, start=1):

    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]

    # Sort by similarity
    top_indices = np.argsort(similarities)[::-1]  # descending
    ordered_docs = [doc_ids[i] for i in top_indices]

    # Save result row
    results.append({
        "query_id": q_id,
        "ordered_doc_ids": " ".join(ordered_docs)
    })

# Write results.csv
with open(results_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["query_id", "ordered_doc_ids"])
    writer.writeheader()
    writer.writerows(results)

print("results.csv created successfully!")
