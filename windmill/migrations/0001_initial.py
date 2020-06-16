# Generated by Django 3.0.7 on 2020-06-16 11:14

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('entity', models.IntegerField(choices=[(0, 'NA-ONE'), (1, 'SWGC'), (2, 'SWGC Member'), (3, 'Company')], db_index=True, default=3, verbose_name='Agency entity type')),
                ('type', models.IntegerField(choices=[(0, 'Normal'), (1, 'Prepaid')], db_index=True, default=0, verbose_name='Pay type')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('weekday_day', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Weekday day')),
                ('weekend_morning', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Weekend morning')),
                ('weekend_afternoon', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Weekend afternoon')),
                ('twilight', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Twilight')),
                ('night', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Night')),
            ],
            options={
                'verbose_name': 'Agency',
                'verbose_name_plural': 'Agencies',
            },
        ),
        migrations.CreateModel(
            name='NaoneAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('asset_type', models.IntegerField(choices=[(0, 'Petty cash'), (1, 'Prepaid'), (2, 'Bank account'), (3, 'E-Coupon')], db_index=True, default=0, verbose_name='Asset type')),
                ('name', models.CharField(max_length=255, verbose_name='Asset name')),
                ('balance', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Asset balance')),
            ],
            options={
                'verbose_name': 'NA-ONE Asset',
                'verbose_name_plural': 'NA-ONE Assets',
            },
        ),
        migrations.CreateModel(
            name='TeeOffTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('customer_name', models.CharField(max_length=255, verbose_name='Customer name')),
                ('pax', models.IntegerField(default=4, verbose_name='Pax')),
                ('hole', models.IntegerField(choices=[(0, '18 Holes'), (1, '9 Holes'), (2, '27 Holes'), (3, '36 Holes')], db_index=True, default=0, verbose_name='No. of holes')),
                ('booking_status', models.IntegerField(choices=[(0, 'order opened'), (1, 'order pending'), (2, 'payment pending'), (3, 'order complete'), (4, 'order offered'), (5, 'order voided'), (6, 'refund requested'), (7, 'refund pending'), (8, 'order refunded(original)'), (9, 'order refunded(reverse)')], db_index=True, default=0, verbose_name='Booking status')),
                ('season', models.IntegerField(choices=[(0, 'Low season'), (1, 'High season')], db_index=True, default=1, verbose_name='High/Low Season')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Weekday'), (1, 'Weekend')], db_index=True, default=0, verbose_name='Day of week')),
                ('slot', models.IntegerField(choices=[(0, 'Morning'), (1, 'Daytime'), (2, 'Twilight'), (3, 'Night')], db_index=True, default=0, verbose_name='Time slot')),
                ('type', models.IntegerField(choices=[(0, 'Fixed'), (1, 'Stand-by')], db_index=True, default=0, verbose_name='Tee off type')),
                ('tee_off_status', models.IntegerField(choices=[(0, 'Open'), (1, 'Held'), (2, 'Sold'), (3, 'Revoked')], db_index=True, default=0, verbose_name='Tee off status')),
                ('day', models.DateField(db_index=True, verbose_name='Round day')),
                ('time', models.TimeField(verbose_name='Tee-off time')),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='windmill.Agency', verbose_name='Agency')),
            ],
            options={
                'verbose_name': 'Tee-off time',
                'verbose_name_plural': 'Tee-off times',
            },
        ),
        migrations.CreateModel(
            name='NaoneManagingBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField(db_index=True, verbose_name='Transaction date')),
                ('memo', models.CharField(max_length=255, verbose_name='Transaction memo')),
                ('asset_type', models.IntegerField(choices=[(0, 'Petty cash'), (1, 'Prepaid'), (2, 'E-Coupon')], db_index=True, default=0, verbose_name='Asset type')),
                ('cash_flow', models.IntegerField(choices=[(0, 'Cash-in'), (1, 'Cash-out')], db_index=True, default=0, verbose_name='Cash flow')),
                ('count', models.IntegerField(default=0, verbose_name='Count')),
                ('amount', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Amount')),
                ('input_type', models.IntegerField(choices=[(0, 'Manual input'), (1, 'Closing input')], db_index=True, default=0, verbose_name='Input type')),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='windmill.Agency', verbose_name='Agency')),
            ],
            options={
                'verbose_name': 'NA-ONE Managing Book',
                'verbose_name_plural': 'NA-ONE Managing Book',
            },
        ),
        migrations.CreateModel(
            name='NaoneAssetTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('fee', models.IntegerField(choices=[(0, 'Green fee'), (1, 'Caddie fee'), (2, 'Cart fee'), (3, 'Promotion')], db_index=True, default=0, verbose_name='Fee')),
                ('cash_flow', models.IntegerField(choices=[(0, 'Cash-in'), (1, 'Cash-out')], db_index=True, default=0, verbose_name='Cash flow')),
                ('input_type', models.IntegerField(choices=[(0, 'Manual input'), (1, 'Closing input')], db_index=True, default=0, verbose_name='Input type')),
                ('unit_price', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Unit price')),
                ('amount', models.DecimalField(decimal_places=0, default=Decimal('0'), help_text='THB', max_digits=11, verbose_name='Amount')),
                ('transaction_date', models.DateTimeField(verbose_name='Transaction date')),
                ('remarks', models.TextField(blank=True, verbose_name='Remarks')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='windmill.NaoneAsset', verbose_name='Asset')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='windmill.TeeOffTime', verbose_name='Tee-off')),
            ],
            options={
                'verbose_name': 'Asset transaction',
                'verbose_name_plural': 'Asset transactions',
            },
        ),
    ]
