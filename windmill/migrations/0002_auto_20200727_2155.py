# Generated by Django 3.0.8 on 2020-07-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windmill', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teeofftime',
            name='phone',
            field=models.CharField(blank=True, max_length=32, verbose_name='Telephone'),
        ),
        migrations.AddField(
            model_name='teeofftime',
            name='remarks',
            field=models.TextField(blank=True, verbose_name='Remarks'),
        ),
    ]