# Generated by Django 4.1 on 2022-09-05 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0009_tourview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourview',
            name='tour',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='travel.tour'),
        ),
    ]
