# Generated by Django 5.2.4 on 2025-07-23 06:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("umuganda", "0002_initial"),
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="umugandasession",
            options={"ordering": ["-date"]},
        ),
        migrations.AddField(
            model_name="umugandasession",
            name="cell",
            field=models.ForeignKey(
                blank=True,
                help_text="Cell where Umuganda will be held (added by Cell admin)",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="umuganda_sessions",
                to="users.cell",
            ),
        ),
        migrations.AddField(
            model_name="umugandasession",
            name="fines_policy",
            field=models.TextField(
                blank=True, help_text="Fines for absence or delays", null=True
            ),
        ),
        migrations.AddField(
            model_name="umugandasession",
            name="tools_needed",
            field=models.TextField(
                blank=True, help_text="Tools required for the session", null=True
            ),
        ),
        migrations.AddField(
            model_name="umugandasession",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="umugandasession",
            name="updated_by_cell_admin",
            field=models.ForeignKey(
                blank=True,
                help_text="Cell admin who updated details",
                limit_choices_to={"user_level": "cell_officer"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cell_updated_sessions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="umugandasession",
            name="village",
            field=models.ForeignKey(
                blank=True,
                help_text="Optional village where the Umuganda will take place",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="umuganda_sessions",
                to="users.village",
            ),
        ),
        migrations.AlterField(
            model_name="umugandasession",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                help_text="Sector admin who initiated the Umuganda date",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sector_created_sessions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="umugandasession",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="Extra details or description of the activity",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="umugandasession",
            name="sector",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="umuganda_sessions",
                to="users.sector",
            ),
        ),
    ]
