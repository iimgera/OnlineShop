from django.urls import path
from api.v1.views.cart import AddToCartView, ViewCartView, RemoveFromCartView, ClearCartView


urlpatterns = [
    path("add-cart/", AddToCartView.as_view()),
    path("get-cart/", ViewCartView.as_view()),
    path('remove-from-cart/<int:product_id>/', RemoveFromCartView.as_view()),
    path("remove-all/", ClearCartView.as_view()),

]