# Generated by Django 5.2.4 on 2025-07-27 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("umuganda", "0009_remove_umugandasession_cell_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cellumugandasession",
            name="other_details",
            field=models.TextField(blank=True, null=True),
        ),
    ]
