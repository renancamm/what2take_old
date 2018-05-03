from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    DAYS_BASE = 7
    DAYS_LIMIT = 11
    SEX_CHOICES = (
        ('m', 'Homem'),
        ('f', 'Mulher'),
        ('u', 'Unisex'),
    )

    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='u')
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


class Travel(models.Model):
    TEMPERATURE_CHOICES = (
        (0, 'Muito frio'),
        (10, 'Frio'),
        (20, 'Quente'),
        (30, 'Muito quente'),
    )
    RAINY_CHOICES = (
        (0, 'Nenhuma chance'),
        (100, 'Chuva com certeza'),
    )
    LENGTH_CHOICES = (
        (3, '3 dias'),
        (7, '7 dias'),
        (11, '11 dias'),
        (14, '+14 dias'),
    )
    SEX_CHOICES = (
        ('m', 'Homem'),
        ('f', 'Mulher'),
    )

    temperature = models.IntegerField(choices=TEMPERATURE_CHOICES, default=20)
    rainy = models.IntegerField(choices=RAINY_CHOICES, default=0)
    length = models.IntegerField(choices=LENGTH_CHOICES, default=7)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='f')
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return '%s %s %s %s %s' % (self.temperature, self.rainy, self.length, self.sex, self.created_at)
