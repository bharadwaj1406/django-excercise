# Generated by Django 5.2.3 on 2025-06-12 07:48

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("country_code", models.CharField(max_length=10)),
                ("currency_symbol", models.CharField(max_length=10)),
                ("phone_code", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("state_code", models.CharField(max_length=10)),
                ("gst_code", models.CharField(max_length=10)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="states",
                        to="backend.country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("state_code", models.CharField(max_length=10)),
                ("gst_code", models.CharField(max_length=10)),
                ("phone_code", models.CharField(max_length=5)),
                ("city_code", models.CharField(max_length=10, unique=True)),
                ("population", models.PositiveIntegerField()),
                ("avg_age", models.FloatField()),
                ("num_of_adult_males", models.PositiveIntegerField()),
                ("num_of_adult_females", models.PositiveIntegerField()),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cities",
                        to="backend.state",
                    ),
                ),
            ],
        ),
    ]
