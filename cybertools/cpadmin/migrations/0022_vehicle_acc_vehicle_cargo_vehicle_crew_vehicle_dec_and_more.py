# Generated by Django 5.0.1 on 2024-01-16 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpadmin', '0021_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='acc',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='cargo',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='crew',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='dec',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='man',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='passengers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='range',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='top_speed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='sdp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='sp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='weight',
            field=models.FloatField(default=0),
        ),
    ]
