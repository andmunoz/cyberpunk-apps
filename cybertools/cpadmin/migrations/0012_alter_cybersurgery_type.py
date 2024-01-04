# Generated by Django 4.2.5 on 2024-01-04 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpadmin', '0011_cybersurgery_cyberware'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cybersurgery',
            name='type',
            field=models.CharField(choices=[('NO', 'No Aplica'), ('IN', 'Insignificante'), ('SE', 'Secundaria'), ('IM', 'Importante'), ('CR', 'Crítica')], max_length=2),
        ),
    ]
