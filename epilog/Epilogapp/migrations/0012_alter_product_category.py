# Generated by Django 5.2 on 2025-04-28 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Epilogapp', '0011_alter_customuser_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('化粧水', '化粧水'), ('乳液', '乳液'), ('美容液', '美容液'), ('クリーム', 'クリーム')], max_length=100, verbose_name='カテゴリ'),
        ),
    ]
