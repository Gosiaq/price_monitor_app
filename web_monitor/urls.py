from django.contrib import admin
from django.urls import path
from products.views import product_index, trigger_spider, product_price_history_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_index, name='product_index'), # Main page
    path('run/', trigger_spider, name='trigger_spider'),
    path('api/price-history/<int:product_id>/', product_price_history_api, name='price_history_api')
]
