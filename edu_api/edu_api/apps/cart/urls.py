from django.urls import path

from cart import views

urlpatterns = [
    path("option/", views.CartViewSet.as_view({"post": "add_cart",
                                               "get": "list_cart",
                                               "delete": "del_cart_goods",
                                               "patch": "patch_goods",
                                               "put": "select_goods"})),
    path("order/", views.CartViewSet.as_view({"get": "get_select_course"})),

]