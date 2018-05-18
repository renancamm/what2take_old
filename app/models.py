import uuid
from django.db import models
from django.utils.html import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product/', default='product-placeholder.png')

    for_male = models.BooleanField(default=True)
    for_female = models.BooleanField(default=True)
    multiply_by_days = models.BooleanField(default=False)

    qtd_cold = models.FloatField(default=0)
    qtd_cool = models.FloatField(default=0)
    qtd_warm = models.FloatField(default=0)
    qtd_hot = models.FloatField(default=0)

    is_backpack = models.BooleanField(default=False)
    trip_duration = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

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
    DAYS_BASE = 7
    DAYS_LIMIT = 11

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

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    temp = models.IntegerField(choices=TEMP_CHOICES, default=20)
    days = models.IntegerField(choices=DAYS_CHOICES, default=7)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='f')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def add_products(self):
        # Get all product list by gender
        if self.sex == 'm':
            products = Product.objects.filter(for_male=True)
        elif self.sex == 'f':
            products = Product.objects.filter(for_female=True)

        # Split what is product item and what is a backpack item
        products_backpacks = products.exclude(is_backpack=False)
        products_items = products.exclude(is_backpack=True)

        # Get the first backpack that match the trip duration
        if self.days <= 3:
            self.product = products_backpacks.filter(trip_duration__lte=3).first()
        elif self.days <= 7:
            self.product = products_backpacks.filter(trip_duration__lte=7).first()
        else:
            self.product = products_backpacks.filter(trip_duration__gt=7).first()

        # Loop through all products in the list
        for product in products_items:

            # Find the base qtd for this temperature range
            qtd = self.get_product_base_qtd(product, self.temp)

            # Add products that have at lease 1 qtd
            if qtd > 0:

                # If True, let's multiply the qtd by days
                if product.multiply_by_days:
                    qtd = self.multiply_qtd_by_days(product, qtd, self.days)

                # Add product with the right qtd
                BackpackItem.objects.create(backpack=self, product=product, qtd=qtd)

    def get_product_base_qtd(self, product, temp):
        if temp < 10:
            qtd = product.qtd_cold
        elif temp < 20:
            qtd = product.qtd_cool
        elif temp < 30:
            qtd = product.qtd_warm
        else:
            qtd = product.qtd_hot
        return qtd

    def multiply_qtd_by_days(self, product, qtd, days):
        # So let's multiply by how many days?
        days = self.days

        # After the days limit, just do you laundry
        if days > self.DAYS_LIMIT:
            days = self.DAYS_LIMIT

        # Apply multiplier and round it down
        multiplier = days / self.DAYS_BASE
        qtd = int(qtd * multiplier)

        # Minimum qtd is 1 for multiplied bases
        if qtd < 1:
            qtd = 1
        return qtd

    def __str__(self):
        return '%s %s %s %s' % (self.temp, self.days, self.sex, self.created_at)


class BackpackItem(models.Model):
    backpack = models.ForeignKey(Backpack, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qtd = models.IntegerField(default=0)

    def __str__(self):
        return '%sx %s' % (self.qtd, self.product)
