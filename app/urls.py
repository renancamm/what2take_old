from django.urls import path
from . import views


urlpatterns = [
    path('', views.backpack_new, name='backpack-new'),
    path('backpack/<int:backpack_id>/', views.backpack_detail, name='backpack-detail'),
    path('backpack/<int:backpack_id>/product/<int:product_id>', views.product_detail, name='product-detail'),
]
