# Generated by Django 2.1.3 on 2018-12-02 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20181202_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backpack',
            name='place',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]