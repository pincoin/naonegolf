# Generated by Django 3.0.2 on 2020-02-29 03:09

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('windmill', '0003_auto_20200229_0112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('type', models.IntegerField(choices=[(0, 'Normal'), (1, 'Prepaid')], db_index=True, default=0, verbose_name='Pay type')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('weekday_day', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Weekday day')),
                ('weekend_morning', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Weekday morning')),
                ('weekend_afternoon', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Weekday afternoon')),
                ('twilight', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Twilight')),
                ('night', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Night')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='booking',
            name='agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='windmill.Agency', verbose_name='Agency'),
        ),
    ]
