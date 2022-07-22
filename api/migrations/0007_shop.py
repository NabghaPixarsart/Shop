# Generated by Django 4.0.6 on 2022-07-21 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_coreuser_is_valid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid3, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('location', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'shop_1',
                'db_table': 'shop',
            },
        ),
    ]
