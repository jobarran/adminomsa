# Generated by Django 4.1.1 on 2022-10-22 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operario', '0006_presentismo_cargado'),
    ]

    operations = [
        migrations.AddField(
            model_name='dia',
            name='slug',
            field=models.SlugField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]
