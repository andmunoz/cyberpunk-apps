# Generated by Django 4.2.5 on 2023-11-28 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpadmin', '0002_rename_descripción_brand_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='code',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
