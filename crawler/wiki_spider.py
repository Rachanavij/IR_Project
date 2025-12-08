import scrapy
import uuid
import os
import json
from urllib.parse import urljoin


class WikiSpider(scrapy.Spider):
    name = "wiki_spider"

    # Seed URL
    start_urls = ["https://en.wikipedia.org/wiki/Data_science"]

    # Crawler limits
    max_pages = 10
    max_depth = 1

    # Internal counters
    page_count = 0

    # Output folders
    output_dir = "../html_docs"
    mapping_file = "../url_mapping.json"

    # Store mappings
    url_to_id = {}

    def parse(self, response):
        if self.page_count >= self.max_pages:
            return

        # Create unique ID for the document
        doc_id = str(uuid.uuid4()) + ".html"
        file_path = os.path.join(self.output_dir, doc_id)

        # Save HTML
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Store in mapping
        self.url_to_id[response.url] = doc_id

        self.page_count += 1
        self.logger.info(f"Saved: {file_path}")

        # Stop if depth exceeded
        current_depth = response.meta.get("depth", 0)
        if current_depth >= self.max_depth:
            return

        # Extract & follow links
        for link in response.css("a::attr(href)").getall():
            if link.startswith("/wiki/"):
                absolute_url = urljoin("https://en.wikipedia.org/", link)
                yield response.follow(absolute_url, callback=self.parse)

    def closed(self, reason):
        """Write URL → document ID mapping"""
        with open(self.mapping_file, "w") as f:
            json.dump(self.url_to_id, f, indent=4)
        self.logger.info("URL mapping saved.")
