from decimal import Decimal

import logging

import scrapy


class OsSpider(scrapy.Spider):
    name = "ostrov-shop.by"
    start_urls = ["https://ostrov-shop.by/catalog/bytovaya-khimiya/"]

    def parse(self, response, **kwargs):
        for product in response.css(".catalog_block .catalog_item"):
            try:
                price = product.css(".main_price .cost prices::text").get().strip()
                price = Decimal(price.replace(",", "."))
            except Exception:
                price = 0

            data = {
                "external_id": product.attrib.get("data-ga-product-id"),
                "title": product.css(".item-title title-heigh .title::text").get().strip(),
                "price": price,
                "link": f"https://ostrov-shop.by{product.css('a.fancy-tovar::attr(href)').get()}",
                "image": product.css(".image_wrapper_block .img-responsive ls-is-cached lazyloaded::attr(scr)").get()
            }
            yield data

        next_page = response.css(".page-nav_box .btn__page-nav:last-child::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)