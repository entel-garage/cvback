# Generated by Django 4.2.5 on 2023-12-29 13:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0005_alert_remove_telegramalert_events_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="boundingbox",
            name="related_event",
        ),
        migrations.RemoveField(
            model_name="inference",
            name="related_event",
        ),
    ]
