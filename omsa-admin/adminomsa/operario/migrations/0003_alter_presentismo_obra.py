# Generated by Django 4.1.1 on 2022-10-18 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obra', '0001_initial'),
        ('operario', '0002_alter_presentismo_obra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentismo',
            name='obra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='obra.obra'),
        ),
    ]
