import os
import math
import json
from bs4 import BeautifulSoup

# Preprocess HTML content
def clean_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ").lower()

    # remove punctuation
    import re
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # normalize spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Build inverted index with TF-IDF
def build_index(input_folder="html_docs", output_file="index.json"):
    documents = {}
    vocab = {}

    # Read files
    for filename in os.listdir(input_folder):
        if filename.endswith(".html"):
            doc_id = filename.replace(".html", "")
            filepath = os.path.join(input_folder, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()

            cleaned = clean_text(html)
            words = cleaned.split()

            documents[doc_id] = words  # store tokens


    # Compute DF
    df = {}
    for doc_id, words in documents.items():
        unique = set(words)
        for w in unique:
            df[w] = df.get(w, 0) + 1

    N = len(documents)

    # Compute TF-IDF
    index = {}

    for doc_id, words in documents.items():
        tf = {}
        for w in words:
            tf[w] = tf.get(w, 0) + 1

        doc_index = {}

        for w, count in tf.items():
            term_tf = count / len(words)
            term_idf = math.log(N / (1 + df[w]))
            doc_index[w] = term_tf * term_idf

        index[doc_id] = doc_index

    # Save index to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)

    print(f"Index built and saved to {output_file}")


if __name__ == "__main__":
    build_index()
