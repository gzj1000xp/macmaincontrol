# Generated by Django 2.1.3 on 2018-12-21 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finderscript',
            name='path',
            field=models.CharField(max_length=1000),
        ),
    ]
