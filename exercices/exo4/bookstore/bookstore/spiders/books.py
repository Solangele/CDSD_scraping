import scrapy
from bookstore.items import BookItem



class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    page_count = 1 
    max_pages = 3
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], 
                            callback=self.parse, 
                            meta={'page_num': 1})

    def parse(self, response):
        current_page_num = response.meta.get('page_num', 1) 
        MAX_PAGES = 3
        books = response.css("article.product_pod")
        rating_map = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}

        for book in books :
            title = book.css("h3 a::attr(title)").get()
            price = book.css("p.price_color::text").get()
            clean_price_text = price.strip().replace('£', '')
            rating = book.css("p.star-rating::attr(class)").get()
            availability = book.css("p.instock.availability::text").getall()
            availability_string = "".join(availability).strip()
            in_stock_bool = ('In stock' in availability_string)
        
            if rating:
                rating_class_list = rating.split()
                rating_word = [c for c in rating_class_list if c != 'star-rating'][0]
                rating = rating_map.get(rating_word, 0)

            yield {
                'title': title,
                'price': clean_price_text,
                'rating': rating,
                'in_stock': in_stock_bool,
                'availability_raw': availability_string, 
            }
        
        next_page_link = response.css("li.next a::attr(href)").get()
    
        if next_page_link is not None and self.page_count < self.max_pages:
            self.page_count += 1 
            next_page_url = response.urljoin(next_page_link)
            self.logger.info(f"Requête pour la page {self.page_count}/{self.max_pages}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)