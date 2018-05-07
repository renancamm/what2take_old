from django.db import models
from django.utils.html import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    DAYS_BASE = 7
    DAYS_LIMIT = 11

    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product/', default='product-placeholder.png')

    for_male = models.BooleanField(default=True)
    for_female = models.BooleanField(default=True)
    multiply_by_days = models.BooleanField(default=True)

    qtd_cold_base = models.FloatField(default=0)
    qtd_cool_base = models.FloatField(default=0)
    qtd_warm_base = models.FloatField(default=0)
    qtd_hot_base = models.FloatField(default=0)

    def get_quantity(self, temp, days):
        # Find the base qtd for this temperature range
        if temp < 10:
            qtd = self.qtd_cold_base
        elif temp < 20:
            qtd = self.qtd_cool_base
        elif temp < 30:
            qtd = self.qtd_warm_base
        else:
            qtd = self.qtd_hot_base

        # Skip days multiplier if False
        if self.multiply_by_days:

            # Multiply only if the base qtd isn't zero
            if qtd > 0:

                # After the days limit, just do you laundry
                if days > self.DAYS_LIMIT:
                    days = self.DAYS_LIMIT

                # Apply multiplier and round it down
                days_multiplier = days / self.DAYS_BASE
                qtd = int(qtd * days_multiplier)

                # Minimum qtd is 1 for multiplied bases
                if qtd < 1:
                    qtd = 1

        # Return zero or multiplied base
        return qtd

    def __str__(self):
        return self.name

    # Show image on Admin interface
    def image_thumb(self, size):
        return mark_safe('<img src="%s" width="%s" />' % (self.image.url, size))

    def image_thumb_small(self):
        return self.image_thumb('50')

    def image_thumb_big(self):
        return self.image_thumb('300')

    image_thumb_small.short_description = 'Thumb'
    image_thumb_big.short_description = 'Thumb'


class Backpack(models.Model):
    TEMP_CHOICES = (
        (0, 'Muito frio'),
        (10, 'Frio'),
        (20, 'Quente'),
        (30, 'Muito quente'),
    )
    DAYS_CHOICES = (
        (3, '3 dias'),
        (7, '7 dias'),
        (11, '11 dias'),
        (14, '+14 dias'),
    )
    SEX_CHOICES = (
        ('m', 'Homem'),
        ('f', 'Mulher'),
    )

    temp = models.IntegerField(choices=TEMP_CHOICES, default=20)
    days = models.IntegerField(choices=DAYS_CHOICES, default=7)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='f')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def add_products(self):
        if self.sex == 'm':
            products = Product.objects.filter(for_male=True)

        elif self.sex == 'f':
            products = Product.objects.filter(for_female=True)

        # Loop through all the product catalog filtered by gender
        for product in products:
            qtd = product.get_quantity(self.temp, self.days)

            # Add products that have at lease 1 qtd
            if qtd > 0:
                BackpackItem.objects.create(backpack=self, product=product, qtd=qtd)

    def __str__(self):
        return '%s %s %s %s' % (self.temp, self.days, self.sex, self.created_at)


class BackpackItem(models.Model):
    backpack = models.ForeignKey(Backpack, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qtd = models.IntegerField(default=0)

    def __str__(self):
        return '%sx %s' % (self.qtd, self.product)
