# Generated by Django 3.2.10 on 2021-12-17 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogauthor',
            name='bio',
            field=models.TextField(help_text='Enter a short bio', max_length=1000),
        ),
    ]
