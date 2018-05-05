from django.contrib import admin
from .models import Category, Product, Backpack


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'sex',
        'multiply_by_days',
        'qtd_cold_base',
        'qtd_cool_base',
        'qtd_warm_base',
        'qtd_hot_base'
    )


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Backpack)
