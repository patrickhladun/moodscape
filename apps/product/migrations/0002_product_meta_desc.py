# Generated by Django 5.0.7 on 2024-09-14 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='meta_desc',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
