# Generated by Django 3.0.5 on 2020-05-22 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='Blogpost',
        ),
    ]
