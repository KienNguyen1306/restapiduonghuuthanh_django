# Generated by Django 4.1.4 on 2022-12-21 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_rating_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rate',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
