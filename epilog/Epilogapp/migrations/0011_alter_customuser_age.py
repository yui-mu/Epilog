# Generated by Django 5.2 on 2025-04-23 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Epilogapp', '0010_rename_profile_concerns_customuser_concerns_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='年齢'),
        ),
    ]
