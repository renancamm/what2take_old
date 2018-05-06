from django.contrib import admin
from .models import Category, Product, Backpack, BackpackItem


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'for_male',
        'for_female',
        'multiply_by_days',
        'qtd_cold_base',
        'qtd_cool_base',
        'qtd_warm_base',
        'qtd_hot_base'
    )


class BackpackItemInline(admin.TabularInline):
    model = BackpackItem


class BackpackAdmin(admin.ModelAdmin):
    inlines = [
        BackpackItemInline,
    ]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Backpack, BackpackAdmin)
