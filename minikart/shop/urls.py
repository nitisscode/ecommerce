from . import views 
from django.urls import path

urlpatterns = [
    path("category/",views.categoryViewSet.as_view(),name="add_category"),
    path("category/<int:pk>/",views.category_details.as_view(),name="edit_category"),
    path("signup/",views.user_signup.as_view(),name="sigunup"),
    path("login/",views.user_login.as_view(),name="login"),
    path("logout/",views.user_logout.as_view(),name="logout"),
    path("add-product/",views.create_product.as_view(),name="add_product"),
    path("add-product/<int:pk>",views.edit_product.as_view(),name="edit_product"),
    path("products/",views.show_products.as_view(),name="show_products"),
    path("products/<int:pk>/",views.CartItemCreateView.as_view(),name="add_cartproduct"),
    path("orders/",views.OrderListCreateView.as_view(),name="orders"),
    path('cart/', views.CartDetailView.as_view(), name='cart-detail'),
    #path('cart/items/', views.CartItemCreateView.as_view(), name='cart-item-create'),
    path('cart/<int:pk>/', views.CartItemUpdateDeleteView.as_view(), name='cart-item-detail'),
]
