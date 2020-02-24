# Generated by Django 3.0.2 on 2020-02-24 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windmill', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teeofftime',
            name='status',
            field=models.IntegerField(choices=[(0, 'Open'), (1, 'Held'), (2, 'Sold'), (3, 'Revoked')], db_index=True, default=0, verbose_name='Tee off status'),
        ),
    ]