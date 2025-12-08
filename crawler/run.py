from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from wiki_spider import WikiSpider

process = CrawlerProcess(get_project_settings())
process.crawl(WikiSpider)
process.start()
