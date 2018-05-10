from django.contrib import admin
from .models import Category, Product, Backpack, BackpackItem


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'image_thumb_small',
        'name',
        'category',
        'for_male',
        'for_female',
        'multiply_by_days',
        'qtd_cold',
        'qtd_cool',
        'qtd_warm',
        'qtd_hot',
    )
    list_display_links = ('name',)
    ordering = ('category', 'name')
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'category',
                'description',
                'image_thumb_big',
                'image',
            )
        }),
        ('Gender disponibility', {
            'fields': (
                'for_male',
                'for_female',
            )
        }),
        ('Quantity', {
            'description': 'Set quantity based on a 7 days trip',
            'fields': (
                'multiply_by_days',
                'qtd_cold',
                'qtd_cool',
                'qtd_warm',
                'qtd_hot',
            )
        }),
        ('Backpack options', {
            'description': 'Use these if this product is a Backpack',
            'fields': (
                'is_backpack',
                'trip_duration',
            )
        })

    )
    readonly_fields = ('image_thumb_big',)


class BackpackItemInline(admin.TabularInline):
    model = BackpackItem


class BackpackAdmin(admin.ModelAdmin):
    inlines = [
        BackpackItemInline,
    ]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Backpack, BackpackAdmin)
