# Generated by Django 4.1 on 2022-09-05 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_tour_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='tour',
        ),
        migrations.AddField(
            model_name='comment',
            name='image_tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='travel.imagetour'),
        ),
    ]
