# Generated by Django 4.1.7 on 2023-03-01 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('co2e', models.DecimalField(decimal_places=4, max_digits=20)),
            ],
        ),
    ]
