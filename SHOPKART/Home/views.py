from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Case, When
from products.models import Product, Category


def home(request):
    best_sellers = Product.objects.filter(
        is_active=True
    ).order_by("-rating")[:8]

    featured_products = Product.objects.filter(
        is_active=True,
        discount__gt=10,
    ).order_by("-discount")[:8]

    new_products = Product.objects.filter(
        is_active=True
    ).order_by("-created_at")[:8]

    categories = Category.objects.all().order_by("name")

    recently_viewed = []
    product_ids = request.session.get("recently_viewed", [])
    if product_ids:
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(product_ids)])
        recently_viewed = Product.objects.filter(
            id__in=product_ids
        ).order_by(preserved)[:10]

    return render(
        request,
        "Home.html",
        {
            "best_sellers": best_sellers,
            "featured_products": featured_products,
            "new_products": new_products,
            "categories": categories,
            "recently_viewed": recently_viewed,
        }
    )


def contact(request):
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def faq(request):
    return render(request, "faq.html")


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def server_error(request):
    return render(request, "500.html", status=500)
