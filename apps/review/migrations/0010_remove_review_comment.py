# Generated by Django 5.0.7 on 2024-09-30 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0009_alter_review_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='comment',
        ),
    ]
