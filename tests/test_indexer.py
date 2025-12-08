import unittest
import json
from sklearn.feature_extraction.text import TfidfVectorizer


class TestIndexer(unittest.TestCase):
    def setUp(self):
        with open('index.json', 'r', encoding='utf-8') as f:
            self.index = json.load(f)


    def test_index_not_empty(self):
        self.assertTrue(len(self.index) > 0, 'Index is empty')

    def test_tfidf_vectorization(self):
        sample_docs = ["This is a test document.", "Another test document."]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sample_docs)
        self.assertEqual(tfidf_matrix.shape[0], len(sample_docs))


if __name__ == '__main__':
    unittest.main()