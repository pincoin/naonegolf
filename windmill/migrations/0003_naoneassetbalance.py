# Generated by Django 3.0.8 on 2020-07-31 13:22

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('windmill', '0002_auto_20200727_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='NaoneAssetBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('year_month', models.DateField(db_index=True, verbose_name='Year month')),
                ('amount', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Amount')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='windmill.NaoneAsset', verbose_name='Asset')),
            ],
            options={
                'verbose_name': 'NA-ONE Asset Balance',
                'verbose_name_plural': 'NA-ONE Asset Balance',
                'unique_together': {('year_month', 'amount')},
            },
        ),
    ]
