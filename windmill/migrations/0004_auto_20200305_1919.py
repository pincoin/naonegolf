# Generated by Django 3.0.2 on 2020-03-05 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windmill', '0003_auto_20200305_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naonemanagingbook',
            name='account',
        ),
        migrations.AddField(
            model_name='agency',
            name='entity',
            field=models.IntegerField(choices=[(0, 'Na-ONE'), (1, 'SWGC'), (2, 'SWGC Member'), (3, 'Company')], db_index=True, default=3, verbose_name='Agency entity type'),
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
