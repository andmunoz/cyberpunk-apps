# Generated by Django 4.2.5 on 2024-01-04 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpadmin', '0009_brand_type_category_type_weapon_description_armor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='armor',
            name='type',
            field=models.CharField(choices=[('S', 'Blando'), ('H', 'Duro')], default='H', max_length=1),
        ),
        migrations.CreateModel(
            name='Gear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('availability', models.CharField(choices=[('E', 'Excelente'), ('C', 'Común'), ('P', 'Mala'), ('R', 'Rara'), ('A', 'Solo Militares'), ('X', 'Experimental')], default='C', max_length=1)),
                ('type', models.CharField(choices=[('OPT', 'Opcional')], default='OPT', max_length=3)),
                ('weight', models.FloatField()),
                ('cost', models.IntegerField()),
                ('description', models.CharField(max_length=255, null=True)),
                ('image', models.CharField(max_length=255, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpadmin.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpadmin.category')),
            ],
        ),
    ]
