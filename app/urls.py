from django.urls import path
from . import views


urlpatterns = [
    path('', views.backpack_new, name='backpack-new'),
    path('backpack/<uuid:backpack_uuid>/', views.backpack_detail, name='backpack-detail'),
    path('backpack/<uuid:backpack_uuid>/product/<int:product_id>', views.product_detail, name='product-detail'),
]
