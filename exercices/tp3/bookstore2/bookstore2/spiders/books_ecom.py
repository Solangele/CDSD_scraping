import scrapy
from bookstore2.items import BookItem
import re


class BooksEcomSpider(scrapy.Spider):
    name = "books_ecom"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_categories)


    def parse(self, response):
        self.logger.info("Début du scraping : Extraction des liens de catégories...")
        category_links = response.css('ul.nav-list a::attr(href)').getall()
        
        for link in category_links:
            category_url = response.urljoin(link)
            yield scrapy.Request(url=category_url, 
                                 callback=self.parse_category)
                                 
        self.logger.info(f"Requêtes lancées pour {len(category_links)} catégories.")


# scrapy crawl books -O output/books.csv
# scrapy crawl books -O output/books.json