import scrapy
from datetime import datetime
from monitor_ofert.items import ProductItem
from monitor_ofert.selectors_map import SELECTOR_MAP

class ShopSpider(scrapy.Spider):
    name = "shop_spider"

    def __init__(self, category="all", *args, **kwargs):
        super(ShopSpider, self).__init__(*args, **kwargs)
        self.target_category = category

    def start_requests(self):
        for domain, config in SELECTOR_MAP.items():
            if self.target_category == "all" or config.get('category') == self.target_category:
                yield scrapy.Request(
                    url=config['start_url'],
                    callback=self.parse,
                    meta={'domain': domain}
                )

    def parse(self, response):
        domain = response.meta['domain']
        mapping = SELECTOR_MAP.get(domain)
        products = response.css(mapping['container'])

        for p in products:
            item = ProductItem()
            item['name'] = p.css(mapping['name']).get('').strip()
            item['price'] = p.css(mapping['price']).get('').strip()
            item['url'] = response.urljoin(p.css(mapping['link']).get())
            item['shop'] = domain
            item['category'] = mapping.get('category', 'general')
            item['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # określenie waluty
            raw_currency = p.css(mapping['currency']).get('').upper()
            if 'ZŁ' in raw_currency or 'PLN' in raw_currency:
                item['currency'] = 'PLN'
            elif raw_currency:
                item['currency'] = raw_currency
            else:
                item['currency'] = 'PLN'
            img_sel = mapping.get('image_url')
            if img_sel:
                raw_img = p.css(img_sel).get()
                item['image_url'] = response.urljoin(raw_img) if raw_img else None
            yield item