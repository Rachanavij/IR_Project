import os
import json
import pickle
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer

HTML_DIR = "html_docs"
INDEX_FILE = "index.json"

def load_documents():
    docs = []
    doc_ids = []

    for filename in os.listdir(HTML_DIR):
        if filename.endswith(".html"):
            doc_id = filename.replace(".html", "")
            doc_ids.append(doc_id)

            file_path = os.path.join(HTML_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            text = soup.get_text(separator=" ", strip=True)
            docs.append(text)

    return doc_ids, docs

def build_index(doc_ids, documents):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Build inverted index
    index = {}
    feature_names = vectorizer.get_feature_names_out()

    for term_idx, term in enumerate(feature_names):
        postings = {}
        column = tfidf_matrix[:, term_idx].toarray().flatten()

        for doc_index, score in enumerate(column):
            if score > 0:
                postings[doc_ids[doc_index]] = float(score)

        index[term] = postings

    return index, vectorizer, tfidf_matrix

if __name__ == "__main__":
    print("Loading HTML documents...")
    doc_ids, documents = load_documents()

    print("Building TF-IDF index...")
    index, vectorizer, tfidf_matrix = build_index(doc_ids, documents)

    # Save index
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=4)

    # Save TF-IDF model + matrix
    with open("vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    with open("tfidf_matrix.pkl", "wb") as f:
        pickle.dump(tfidf_matrix, f)

    with open("doc_ids.json", "w") as f:
        json.dump(doc_ids, f, indent=4)

    print("\nIndexing completed successfully!")
    print(f"Indexed {len(doc_ids)} documents.")
