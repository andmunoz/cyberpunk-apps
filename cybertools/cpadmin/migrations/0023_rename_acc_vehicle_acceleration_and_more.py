# Generated by Django 4.2.5 on 2024-01-17 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpadmin', '0022_vehicle_acc_vehicle_cargo_vehicle_crew_vehicle_dec_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='acc',
            new_name='acceleration',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='dec',
            new_name='deceleration',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='man',
            new_name='maneuverability',
        ),
    ]