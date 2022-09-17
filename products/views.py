from django.core.cache import cache
from django.db.models import Count, F, QuerySet, Sum
from django.shortcuts import render

from django.http import HttpResponse
from products.models import Product


def products(request):
    if request.GET.get("color"):
        product_list = Product.objects.filter(color=request.GET.get("color"))
    else:
        product_list = Product.objects.all()
    order_by = request.GET.get("order_by")

    product_list = product_sorting(product_list, order_by)
    return render(request, "index.html", {"product_list": product_list})


def product_sorting(queryset: QuerySet, order_by: str):
    if order_by == "cost":
        return queryset.order_by("cost")
    elif order_by == "-cost":
        return queryset.order_by("cost")
    elif order_by == "sold":
        queryset = queryset.annotate(sold=Sum(F("cost") * F("purchase__count")))
        return queryset.order_by("sold")
    elif order_by == "popular":
        queryset = queryset.annotate(popular=Sum("purchase__count"))
        return queryset.order_by("popular")
    return queryset
