# Generated by Django 4.1 on 2022-08-26 07:49

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_alter_tag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='note',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
