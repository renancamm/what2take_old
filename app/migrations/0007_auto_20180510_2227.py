# Generated by Django 2.0.4 on 2018-05-10 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180510_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productbackpack',
            name='product_ptr',
        ),
        migrations.AddField(
            model_name='product',
            name='backpack_for_duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='is_backpack',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='multiply_by_days',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ProductBackpack',
        ),
    ]
