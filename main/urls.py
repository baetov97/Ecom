from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='main'),

    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    path('update_item/', UpdateItemView.as_view(), name='update_item'),
    path('process_order/', ProcessOrder.as_view(), name='process_order'),

    path('search/', SearchResultView.as_view(), name='search_result'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),

    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
