# Generated by Django 2.0.4 on 2018-05-17 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_backpack_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
    ]