# Generated by Django 4.0.6 on 2022-07-21 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_coreuser_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coreuser',
            old_name='core_id',
            new_name='id',
        ),
    ]
