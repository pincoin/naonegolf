# Generated by Django 3.0.2 on 2020-03-05 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windmill', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naonemanagingbook',
            name='memo',
            field=models.CharField(max_length=255, verbose_name='Transaction memo'),
        ),
    ]
