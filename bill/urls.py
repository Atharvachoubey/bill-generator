from django.urls import path
from .views import bill_form, generate_bill

urlpatterns = [

    path("", bill_form, name="bill_form"),

    path(
        "generate-bill/",
        generate_bill,
        name="generate_bill"
    ),

]