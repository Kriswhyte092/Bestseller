from django.urls import path
from .views import (
    noos_view as noos,
    noos_info_view as noos_info,
    get_inventory_for_variant,
)


urlpatterns = [
    path("", noos, name="noos"),
    path("noos-info/", noos_info, name="noos_info"),
    path(
        "get-variant-inventory/",
        get_inventory_for_variant,
        name="get_variant_inventory",
    ),
]
