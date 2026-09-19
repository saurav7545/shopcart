from django.urls import path
from . import views


urlpatterns = [

    path(
        "search/",
        views.search,
        name="search"
    ),

    path(
        "category/<slug:slug>/",
        views.category,
        name="category"
    ),

    path(
        "<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "<int:product_id>/review/",
        views.add_review,
        name="add_review"
    ),
]