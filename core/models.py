from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Travel(models.Model):
    TEMPERATURE_CHOICES = (
        (-5, 'Muito frio'),
        (10, 'Frio'),
        (20, 'Quente'),
        (35, 'Muito quente'),
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
        ('m', 'male'),
        ('f', 'female'),
    )

    temperature = models.IntegerField(choices=TEMPERATURE_CHOICES, default=20)
    rainy = models.IntegerField(choices=RAINY_CHOICES, default=0)
    length = models.IntegerField(choices=LENGTH_CHOICES, default=7)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='f')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return '%s %s %s %s %s' % (self.temperature, self.rainy, self.length, self.sex, self.created_at)
