# Generated by Django 4.1.4 on 2022-12-08 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_couses_options_couses_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='couses',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='couses_id',
            new_name='couses',
        ),
        migrations.AlterUniqueTogether(
            name='couses',
            unique_together={('sub', 'category')},
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('sub', 'couses')},
        ),
    ]
