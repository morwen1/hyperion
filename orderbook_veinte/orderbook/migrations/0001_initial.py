# Generated by Django 3.0.5 on 2020-05-20 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('uptadeted_at', models.DateTimeField(null=True)),
                ('orderId', models.AutoField(help_text='id of the Trade auto increment field', primary_key=True, serialize=False)),
                ('traderId', models.CharField(max_length=255)),
                ('timestamp', models.TimeField()),
                ('qty', models.IntegerField()),
                ('price', models.FloatField()),
                ('close_qty', models.IntegerField(null=True)),
                ('Bid', models.BooleanField(default=False)),
                ('Ask', models.BooleanField(default=False)),
                ('market_qty', models.CharField(max_length=255)),
                ('market_price', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('uptadeted_at', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('uptadeted_at', models.DateTimeField(null=True)),
                ('qty', models.FloatField()),
                ('price', models.FloatField()),
                ('timestamp', models.TimeField()),
                ('p1_traderId', models.CharField(max_length=255)),
                ('p1_side', models.CharField(max_length=255)),
                ('p1_orderId', models.CharField(max_length=255)),
                ('p2_traderId', models.CharField(max_length=255)),
                ('p2_side', models.CharField(max_length=255)),
                ('p2_orderId', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('uptadeted_at', models.DateTimeField(null=True)),
                ('type_transaction', models.CharField(choices=[('partial', 'complete')], max_length=120)),
                ('qty', models.IntegerField()),
                ('price', models.FloatField()),
                ('market_qty', models.CharField(max_length=255)),
                ('market_price', models.CharField(max_length=255)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_buyer', to='orderbook.Orders')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_seller', to='orderbook.Orders')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orderbook.OrderStatus'),
        ),
    ]
