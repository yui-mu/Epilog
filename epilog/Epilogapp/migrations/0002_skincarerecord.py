# Generated by Django 5.2 on 2025-04-13 01:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Epilogapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkincareRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField(verbose_name='記録日')),
                ('skin_condition', models.TextField(blank=True, verbose_name='肌の状態メモ')),
                ('skin_rating', models.IntegerField(choices=[(1, 'とても良い'), (2, '良い'), (3, '普通'), (4, 'やや悪い'), (5, '悪い')], verbose_name='肌の調子')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='肌の写真')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
