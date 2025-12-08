# CS429 - Information Retrieval

## Individual Project

Name: Rachana Vijay

CWID: A20605843

---

## 1. Project Description

This project implements a minimal IR system that crawls web pages, builds an inverted index using TF-IDF, and ranks documents based on cosine similarity for user queries. It supports batch query processing via CSV and outputs top-K ranked documents.

**Key Features:**

* HTML content crawling from Wikipedia (Data Science pages)
* TF-IDF based indexing
* Cosine similarity ranking
* Flask server for handling CSV queries
* Top-K results generation

---

## 2. Full Project Structure

```
IR_Project/
│
├── html_docs/                   # Crawled HTML documents (10 pages from seed URL)
│   ├── page1.html
│   ├── page2.html
│   └── ...
│
├── crawler/                     # Scrapy crawler code
│   ├── wiki_spider.py
│   └── run.py
│
├── tests/                       # Test files
│   ├── test_processor.py
│   ├── test_crawler.py
│   └── test_indexer.py
|
├── app.py                       # Flask server for query processing
├── build_index.py               # Build TF-IDF index
├── index.json                   # TF-IDF inverted index
├── docs_ids.json                # Document ID mapping
├── indexer.py                   # Indexing script
├── query_processor.py           # Query processing module
├── queries.csv                  # Sample queries
├── results.csv                  # Generated top-K results
├── requirements.txt             # Python dependencies
├── tfidf_matrix.pkl             # Serialized TF-IDF matrix
├── vectorizer.pkl               # Serialized TF-IDF vectorizer
├── url_mapping.json             # Mapping of crawled URLs to document IDs
├── README.md                    # Project README
└── report.pdf                   # Project report
```

---

## 3. Requirements

* Python 3.12+
* scikit-learn 1.6+
* Flask 3.1+
* Scrapy 2.13+ (optional for crawling)
* NLTK 3.8 (optional)
* Additional packages: numpy, scipy, pandas, beautifulsoup4, python-Levenshtein, tqdm, pickle

Install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4. Installation and Setup

1. Clone or download the repository.
2. Ensure `html_docs/` contains the crawled HTML pages.
3. Activate virtual environment and install dependencies.
4. Build index:

```bash
python indexer.py
```

5. Run Flask server:

```bash
python app.py
```

---

## 5. Usage

* Access Flask server at `http://127.0.0.1:5000`.
* Process queries in CSV format (`queries.csv`):

```bash
curl -X POST -F "file=@queries.csv" http://127.0.0.1:5000/search
```

* Output: `results.csv` with top-3 ranked documents per query.

---

## 6. File Descriptions

| File                 | Description                                                                                     |
| -------------------- | ----------------------------------------------------------------------------------------------- |
| `indexer.py`         | Builds TF-IDF matrix, saves `index.json`, `tfidf_matrix.pkl`, `vectorizer.pkl`, `docs_ids.json` |
| `query_processor.py` | Processes user queries, calculates similarity, returns ranked results                           |
| `app.py`             | Flask server to handle CSV query requests                                                       |
| `html_docs/`         | Crawled HTML pages from seed Wikipedia URL                                                      |
| `index.json`         | TF-IDF inverted index (term → tf-idf per document)                                              |
| `docs_ids.json`      | Maps document IDs to filenames                                                                  |
| `tfidf_matrix.pkl`   | Serialized TF-IDF matrix (documents × terms)                                                    |
| `vectorizer.pkl`     | Serialized TF-IDF vectorizer for query transformation                                           |
| `url_mapping.json`   | Maps original URLs to document IDs                                                              |
| `queries.csv`        | Sample queries for testing                                                                      |
| `results.csv`        | Output top-K results per query                                                                  |

---

## Component Descriptions

### Scrapy Crawler

* Crawls HTML content from Wikipedia starting from a seed URL.
* Configurable parameters: max pages, max depth.
* Saves crawled pages into `html_docs/`.

### Scikit-learn Indexer

* Processes HTML pages to extract text content.
* Builds a TF-IDF matrix and inverted index.
* Serializes matrix (`tfidf_matrix.pkl`) and vectorizer (`vectorizer.pkl`) for efficient query processing.
* Generates `index.json` and `docs_ids.json` for mapping documents and terms.

### Flask Processor

* Accepts CSV queries and validates inputs.
* Computes cosine similarity between query vectors and document TF-IDF vectors.
* Ranks documents and outputs top-K results in `results.csv`.

---

## 7. Test Cases

* **Framework:** pytest
* **Coverage:** Crawler, Indexer, Processor
* **Run tests:**

```bash
python -m pytest
```

* All tests passed successfully (unit tests included for indexing and query processing).

---

## 8. Limitations

* Limited to 10 crawled pages
* TF-IDF ranking only (no semantic search)
* Optional NLP enhancements not implemented

---

## 9. Future Work

* Crawl larger datasets (>100 pages)
* Implement semantic search with embeddings (FAISS)
* Add query expansion, spell correction
* Deploy with production-ready WSGI server

---

## 10. Bibliography

1. Salton, G., & McGill, M. J. *Introduction to Modern Information Retrieval*. McGraw-Hill, 1983.
2. Manning, C. D., Raghavan, P., & Schütze, H. *Introduction to Information Retrieval*. Cambridge University Press, 2008.
3. Goodfellow, I., Bengio, Y., & Courville, A. *Deep Learning*. MIT Press, 2016.
4. Hastie, T., Tibshirani, R., & Friedman, J. *The Elements of Statistical Learning*. Springer, 2009.
5. Wikipedia — [Data Science](https://en.wikipedia.org/wiki/Data_science)
6. *Open AI*, ChatGPT.
