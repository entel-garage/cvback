# Generated by Django 4.2.5 on 2024-06-23 23:36

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import encrypted_field.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Area",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("added_date", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("added_modified", models.DateTimeField(auto_now=True, verbose_name="date modified")),
                ("name", models.CharField(max_length=255)),
                ("diagram", models.ImageField(blank=True, null=True, upload_to="")),
            ],
        ),
        migrations.CreateModel(
            name="InferenceComputer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("added_date", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("added_modified", models.DateTimeField(auto_now=True, verbose_name="date modified")),
                ("enabled", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        default=django.contrib.gis.geos.point.Point(
                            -70.69441297829056, -33.358564373936446, srid=4326
                        ),
                        srid=4326,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Camera",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("added_date", models.DateTimeField(auto_now_add=True, verbose_name="date created")),
                ("added_modified", models.DateTimeField(auto_now=True, verbose_name="date modified")),
                ("enabled", models.BooleanField(default=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "primary_stream",
                    encrypted_field.fields.EncryptedField(
                        max_length=1024,
                        validators=[django.core.validators.URLValidator(schemes=["http", "https", "rtsp"])],
                    ),
                ),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        default=django.contrib.gis.geos.point.Point(-70.6561237, -33.4396059, srid=4326), srid=4326
                    ),
                ),
                ("last_seen_online", models.DateTimeField(auto_now=True, verbose_name="last seen online")),
                ("need_cleaning", models.BooleanField(default=False)),
                ("need_physical_maintenance", models.BooleanField(default=False)),
                ("need_replacement", models.BooleanField(default=False)),
                ("photo", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "area",
                    models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="devices.area"),
                ),
            ],
        ),
    ]
