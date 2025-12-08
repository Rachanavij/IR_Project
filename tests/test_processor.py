import unittest
from app import process_queries

class TestApp(unittest.TestCase):
    def setUp(self):
        self.sample_queries = [
            ("q1", "data science"),
            ("q2", "machine learning")
        ]
        self.top_k = 3

    def test_process_queries(self):
        results = process_queries(self.sample_queries, top_k=self.top_k)
        self.assertEqual(len(results), len(self.sample_queries) * self.top_k)
        for res in results:
            self.assertIn('query_id', res)
            self.assertIn('rank', res)
            self.assertIn('document_id', res)

if __name__ == "__main__":
    unittest.main()
