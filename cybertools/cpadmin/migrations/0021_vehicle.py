# Generated by Django 5.0.1 on 2024-01-16 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpadmin', '0020_alter_drug_effects_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('S', 'Blando'), ('H', 'Duro')], default='H', max_length=1)),
                ('sp', models.IntegerField()),
                ('sdp', models.IntegerField()),
                ('weight', models.FloatField()),
                ('cost', models.IntegerField()),
                ('description', models.CharField(max_length=255, null=True)),
                ('image', models.CharField(max_length=255, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpadmin.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpadmin.category')),
            ],
        ),
    ]
