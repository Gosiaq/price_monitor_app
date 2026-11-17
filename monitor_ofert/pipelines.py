import os
import django
import re
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_monitor.settings')
django.setup()

from products.models import Product, PriceHistory

class DjangoDatabasePipeline:
    async def process_item(self, item, spider):
        name = item.get('name', '')
        new_price = self.parse_price(item.get('price', '0'))
        url = item['url']

        # ilość produktów
        m_match = re.search(r'(\d+)\s*[xX]', name)
        m_val = int(m_match.group(1)) if m_match else 1

        # gramatura/objętość
        q_regex = r'(\d+(?:[.,]\d+)?)(?:\s*/\s*\d+(?:[.,]\d+)?)?\s*(kg|g|l|ml|szt)'
        q_match = re.search(q_regex, name, re.IGNORECASE)

        q_val = float(q_match.group(1).replace(',', '.')) if q_match else 0
        unit = q_match.group(2).lower() if q_match else ""
        quantity_str = f"{q_match.group(1)} {unit}" if q_match else ""

        unit_price, unit_measure = self.calculate_unit_price(new_price, q_val, unit, m_val)

        # aktualizacja lub tworzenie produktu
        product = await sync_to_async(Product.objects.filter(url=url).first)()

        if product:
            if float(product.price) != float(new_price):
                # Cena się zmieniła - aktualizacja produktu, wpis do historii
                product.price = new_price
                product.quantity = quantity_str
                product.unit_price = unit_price
                product.unit_measure = unit_measure
                await sync_to_async(product.save)()

                await sync_to_async(PriceHistory.objects.create)(product=product, price=new_price)
        else:
            # Nowy produkt
            product = await sync_to_async(Product.objects.create)(
                url=url,
                name=name,
                price=new_price,
                currency=item.get('currency'),
                multipack=f"{m_val} x",
                quantity=quantity_str,
                unit_price=unit_price,
                unit_measure=unit_measure,
                shop=item['shop'],
                category=item['category'],
                image_url=item.get('image_url'),
            )
            await sync_to_async(PriceHistory.objects.create)(product=product, price=new_price)

        return item

    def calculate_unit_price(self, price, val, unit, m_val):
        if not price or not val: return None, None
        try:
            # Przelicznik na kg/l
            weight_units = ['g', 'kg', 'ml', 'l']

            if unit in weight_units:
                factor = val / 1000 if unit in ['g', 'ml'] else val
                total_weight = m_val * factor

                res = round(price / total_weight, 2) if total_weight > 0 else None
                base_unit = 'l' if unit in ['l', 'ml'] else 'kg'
                return res, base_unit
            else:
                return None, None
        except: return None, None

    def parse_price(self, p):
        p_clean = str(p).lower().replace('od:', '').replace('od', '')
        match = re.search(r'(\d+(?:[.,]\d+)?)', str(p_clean).replace(' ', '').replace('\xa0', ''))
        return float(match.group(1).replace(',', '.')) if match else 0.0