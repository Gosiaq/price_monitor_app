import scrapy

class ProductItem(scrapy.Item):
    # Core product data
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()

    # Categorization and source
    category = scrapy.Field()
    shop = scrapy.Field()

    # Links and media
    url = scrapy.Field()
    image_url = scrapy.Field()

    # Metadata for analytics (for your thesis charts)
    timestamp = scrapy.Field()
    on_sale = scrapy.Field() # Boolean: True if promotion detected