# Generated by Django 5.2.4 on 2025-07-24 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admn", "0007_alter_celladminmembership_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="celladminmembership",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
