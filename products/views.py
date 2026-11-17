from django.shortcuts import render, redirect
from .models import Product, PriceHistory
from .tasks import run_spider
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

def product_index(request):
    CATEGORY_NAMES = {
        'bio_food': 'Zdrowa żywność',
        'cosmetics': 'Kosmetyki',
        'clothing': 'Ubrania',
        'all': 'Wszystkie produkty'
    }

    query = request.GET.get('q')
    category_filter = request.GET.get('cat')
    sort = request.GET.get('sort', '-timestamp')
    products = Product.objects.all().order_by(sort)
    existing_categories = Product.objects.values_list('category', flat=True).distinct()

    categories_with_names = []
    for cat in existing_categories:
        categories_with_names.append({
            'slug': cat,
            'name': CATEGORY_NAMES.get(cat, cat)
        })

    if category_filter:
        products = products.filter(category=category_filter)
    current_category_name = CATEGORY_NAMES.get(category_filter) if category_filter else None

    if query:
        products = [p for p in products if query.lower() in p.name.lower()]
    else:
        products = products[:100]

    return render(request, 'products/index.html', {
        'products': products,
        'query': query,
        'current_sort': sort,
        'categories_with_names': categories_with_names,
        'current_category_name': current_category_name,
        'current_category': category_filter
    })

def trigger_spider(request):
    if request.method == "POST":
        category = request.POST.get('category', 'all')
        run_spider.delay(category=category)
        return redirect('product_index')

def product_price_history_api(request, product_id):
    if request.method != "GET":
        return HttpResponseBadRequest("Nie otrzymano zapytania GET.")

    product = get_object_or_404(Product, id=product_id)
    history = PriceHistory.objects.filter(product=product).order_by('timestamp')

    data = {
        'labels': [h.timestamp.strftime('%d.%m.%Y %H:%M') for h in history],
        'prices': [float(h.price) for h in history],
        'product_name': product.name
    }
    return JsonResponse(data)