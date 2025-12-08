import os
import unittest


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.html_folder = 'html_docs'


    def test_html_files_exist(self):
        files = os.listdir(self.html_folder)
        self.assertGreater(len(files), 0, 'No HTML files found in html_docs/')


    def test_html_file_content(self):
        files = os.listdir(self.html_folder)
        for file in files:
            with open(os.path.join(self.html_folder, file), 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertTrue(len(content) > 0, f'{file} is empty')

if __name__ == '__main__':
    unittest.main()