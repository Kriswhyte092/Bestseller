from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Inventory, Variant


def get_inventory_for_variant(request):
    """
    Fetch and return inventory details for a specific variant.
    """
    variant_id = request.GET.get("variant_id")
    variant = get_object_or_404(Variant, id=variant_id)

    inventory_data = [
        {"store": inv.store.store_name, "quantity": inv.quantity}
        for inv in Inventory.objects.filter(variant=variant)
    ]

    return JsonResponse({"variant_id": variant_id, "inventory": inventory_data})


def noos_view(request):
    """
    View for displaying all NOOS products with their names and images.
    """
    products = Product.objects.all()
    product_data = [
        {
            "name": product.name,
            "image_url": (
                product.color_variants.first().image_urls[0]
                if product.color_variants.exists()
                and product.color_variants.first().image_urls
                else ""
            ),
        }
        for product in products
    ]
    return render(request, "noos/noos.html", {"products": product_data})


def noos_info_view(request):
    """
    View for displaying product details such as color variants, sizes, and inventory.
    """
    product_name = request.GET.get("product")
    product = get_object_or_404(Product, name=product_name)

    color_variants = [
        {
            "color_name": color_variant.colorName,
            "color_code": color_variant.colorCode,
            "images": color_variant.image_urls,
        }
        for color_variant in product.color_variants.all()
    ]

    sizes = {}
    for variant in product.color_variants.prefetch_related("variants").all():
        for v in variant.variants.all():
            inventory = Inventory.objects.filter(variant=v)
            locations = {inv.store.store_name: inv.quantity for inv in inventory}
            if v.size not in sizes:
                sizes[v.size] = {}
            sizes[v.size].update(locations)

    data = {
        "name": product.name,
        "image_urls": [url for color in color_variants for url in color["images"]],
        "colors": {
            color["color_name"]: color["color_code"] for color in color_variants
        },
        "sizes": sizes,
    }

    return render(request, "noos/noos-info.html", data)
