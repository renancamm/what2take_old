from django.urls import path
from . import views


urlpatterns = [
    path('', views.backpack_new, name='backpack-new'),
    path('backpack/<int:id>', views.backpack_detail, name='backpack-detail'),
]
