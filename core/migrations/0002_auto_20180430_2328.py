# Generated by Django 2.0.4 on 2018-04-30 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='products',
            field=models.ManyToManyField(to='core.Product'),
        ),
        migrations.AlterField(
            model_name='travel',
            name='sex',
            field=models.CharField(choices=[('m', 'Homem'), ('f', 'Mulher')], default='f', max_length=1),
        ),
    ]
