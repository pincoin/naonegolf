# Generated by Django 3.0.2 on 2020-03-05 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windmill', '0003_naonemanagingbook_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naonemanagingbook',
            name='date',
            field=models.DateField(db_index=True, verbose_name='Transaction date'),
        ),
    ]
