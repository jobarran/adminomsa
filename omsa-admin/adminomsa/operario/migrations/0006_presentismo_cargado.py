# Generated by Django 4.1.1 on 2022-10-20 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operario', '0005_alter_presentismo_obra'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentismo',
            name='cargado',
            field=models.BooleanField(default=False),
        ),
    ]
