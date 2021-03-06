# Generated by Django 3.0.2 on 2020-01-29 16:11

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
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Golf club name')),
                ('phone', models.CharField(blank=True, max_length=16, null=True, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email address')),
                ('website', models.URLField(blank=True, max_length=255, null=True, verbose_name='Website')),
                ('hole', models.IntegerField(choices=[(0, '18 Holes'), (1, '9 Holes'), (2, '27 Holes'), (3, '36 Holes')], db_index=True, default=0, verbose_name='No. of holes')),
                ('cart_rental_required', models.BooleanField(db_index=True, default=False, verbose_name='Cart rental required')),
                ('cart_fee', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Cart fee')),
                ('caddie_fee', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Caddie fee')),
                ('high_season', models.IntegerField(default=3075, verbose_name='High season')),
                ('max_high_weekday', models.PositiveIntegerField(default=0, verbose_name='Max # of High/Weekday')),
                ('max_high_weekend', models.PositiveIntegerField(default=0, verbose_name='Max # of High/Weekend')),
                ('max_low_weekday', models.PositiveIntegerField(default=0, verbose_name='Max # of Low/Weekday')),
                ('max_low_weekend', models.PositiveIntegerField(default=0, verbose_name='Max # of Low/Weekend')),
                ('country', models.IntegerField(choices=[(1, 'Thailand'), (2, 'South Korea'), (3, 'Japan'), (4, 'China')], db_index=True, default=1, verbose_name='Country code')),
            ],
            options={
                'verbose_name': 'Golf club',
                'verbose_name_plural': 'Golf clubs',
            },
        ),
        migrations.CreateModel(
            name='ClubProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('season', models.IntegerField(choices=[(0, 'Low season'), (1, 'High season')], db_index=True, default=1, verbose_name='High/Low Season')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Weekday'), (1, 'Weekend')], db_index=True, default=0, verbose_name='Day of week')),
                ('slot', models.IntegerField(choices=[(0, 'Morning'), (1, 'Daytime'), (2, 'Twilight'), (3, 'Night')], db_index=True, default=0, verbose_name='Time slot')),
            ],
            options={
                'verbose_name': 'Golf club product',
                'verbose_name_plural': 'Golf club products',
                'unique_together': {('season', 'day_of_week', 'slot')},
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Holiday name')),
                ('holiday', models.DateField(db_index=True, verbose_name='Holiday day')),
                ('country', models.IntegerField(choices=[(1, 'Thailand'), (2, 'South Korea'), (3, 'Japan'), (4, 'China')], db_index=True, default=1, verbose_name='Country code')),
            ],
            options={
                'verbose_name': 'Holiday',
                'verbose_name_plural': 'Holidays',
                'unique_together': {('holiday', 'country')},
            },
        ),
        migrations.CreateModel(
            name='ClubProductListMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(verbose_name='Start time')),
                ('end_time', models.TimeField(verbose_name='End time')),
                ('list_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='List price')),
                ('position', models.IntegerField(verbose_name='Position')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.Club', verbose_name='Golf club')),
                ('product_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.ClubProduct', verbose_name='Product list')),
            ],
            options={
                'verbose_name': 'Product list membership',
                'verbose_name_plural': 'Product list membership',
                'unique_together': {('club', 'product_list')},
            },
        ),
        migrations.AddField(
            model_name='club',
            name='products',
            field=models.ManyToManyField(through='golf.ClubProductListMembership', to='golf.ClubProduct'),
        ),
    ]
