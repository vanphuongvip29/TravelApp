# Generated by Django 4.1 on 2022-09-15 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0010_alter_tourview_tour'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_date']},
        ),
    ]
