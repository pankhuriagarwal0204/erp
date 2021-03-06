# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-01-13 04:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalItemType',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('last_updated', models.DateTimeField(blank=True, editable=False)),
                ('status', models.CharField(choices=[('active', 'active'), ('dead', 'dead'), ('used', 'used')], default='active', max_length=10)),
                ('total_quantity', models.IntegerField(default=0)),
                ('total_issued_quantity', models.IntegerField(default=0, editable=False)),
                ('in_stock_quantity', models.IntegerField(default=0, editable=False)),
                ('quantity_issued', models.IntegerField(blank=True, default=0, null=True)),
                ('issued_on', models.DateTimeField(blank=True, null=True)),
                ('quantity_returned', models.IntegerField(blank=True, default=0, null=True)),
                ('returned_on', models.DateTimeField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('issued_to', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('returned_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical item type',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('available', models.BooleanField(default=True)),
                ('itemname', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('dead', 'dead'), ('used', 'used')], default='active', max_length=10)),
                ('total_quantity', models.IntegerField(default=0)),
                ('total_issued_quantity', models.IntegerField(default=0, editable=False)),
                ('in_stock_quantity', models.IntegerField(default=0, editable=False)),
                ('quantity_issued', models.IntegerField(blank=True, default=0, null=True)),
                ('issued_on', models.DateTimeField(blank=True, null=True)),
                ('quantity_returned', models.IntegerField(blank=True, default=0, null=True)),
                ('returned_on', models.DateTimeField(blank=True, null=True)),
                ('issued_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('returned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returned_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='itemtype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_set', to='inventorysystem.ItemType'),
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
