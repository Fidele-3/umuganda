# Generated by Django 5.2.4 on 2025-07-24 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "umuganda",
            "0003_alter_umugandasession_options_umugandasession_cell_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="fine",
            name="moths_overdue",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="fine",
            name="reason",
            field=models.TextField(blank=True, null=True),
        ),
    ]
