# Generated by Django 5.2 on 2025-04-29 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Epilogapp', '0014_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkinType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
