from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, ProductReview, Category


def search(request):
    query = request.GET.get(
        "q",
        ""
    ).strip()

    products = Product.objects.filter(
        is_active=True
    ).order_by("id")

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().order_by("id")

    paginator = Paginator(products, 12)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(
        request,
        "search.html",
        {
            "products": products,
            "query": query,
        }
    )


def category(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug,
    )

    products = Product.objects.filter(
        category=category,
        is_active=True
    ).order_by("id")

    paginator = Paginator(products, 12)
    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(
        request,
        "mobile.html",
        {
            "products": products,
            "category_name": category.name,
        }
    )


def product_detail(
    request,
    product_id
):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    reviews = product.reviews.select_related(
        "user"
    ).order_by(
        "-created_at"
    )

    recently_viewed = request.session.get("recently_viewed", [])
    if product_id in recently_viewed:
        recently_viewed.remove(product_id)
    recently_viewed.insert(0, product_id)
    request.session["recently_viewed"] = recently_viewed[:10]

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "reviews": reviews,
        }
    )


@login_required
def add_review(
    request,
    product_id
):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    if request.method != "POST":
        return redirect(
            "product_detail",
            product_id=product.id
        )

    rating = request.POST.get(
        "rating"
    )

    comment = request.POST.get(
        "comment",
        ""
    ).strip()

    try:
        rating = int(rating)

    except (TypeError, ValueError):
        messages.error(
            request,
            "Invalid rating."
        )

        return redirect(
            "product_detail",
            product_id=product.id
        )

    if rating < 1 or rating > 5:
        messages.error(
            request,
            "Rating must be between 1 and 5."
        )

        return redirect(
            "product_detail",
            product_id=product.id
        )

    review, created = ProductReview.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={
            "rating": rating,
            "comment": comment,
        }
    )

    reviews = ProductReview.objects.filter(
        product=product
    )

    total_rating = sum(
        review.rating
        for review in reviews
    )

    count = reviews.count()

    product.rating = (
        total_rating / count
        if count
        else 0
    )

    product.save(
        update_fields=["rating"]
    )

    if created:
        messages.success(
            request,
            "Review added successfully."
        )
    else:
        messages.success(
            request,
            "Review updated successfully."
        )

    return redirect(
        "product_detail",
        product_id=product.id
    )
