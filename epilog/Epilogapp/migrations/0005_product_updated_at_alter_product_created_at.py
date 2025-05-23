# Generated by Django 5.2 on 2025-04-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Epilogapp', '0004_concern_ingredient_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新日'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日'),
        ),
    ]
