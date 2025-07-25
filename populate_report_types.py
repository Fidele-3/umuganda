import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import ReportType

# Define your report types exactly as in the model
REPORT_TYPES = [
    ("accident", "Accident"),
    ("government_issue", "Government Issue"),
    ("infastructure_issues", "Infrastructure Issues"),
    ("water_and_sanitary", "Water & Sanitary"),
    ("eletricity", "Electricity"),
    ("health_care", "Healthcare Concerns"),
    ("education", "Education Issue"),
    ("security_and_safety", "Security & Safety"),
    ("corruption_and_mismanagement", "Corruption & Mismanagement"),
    ("public_service_delay_or_neglect", "Public Service Delay Or Neglect"),
    ("environmental_concerns", "Environmental Concerns"),
    ("land_and_property", "Land & Property"),
    ("gender_based_violence", "Gender Based Violence"),
    ("others", "Others"),
    ("genocide_denial_or_ideas_leading_to_it", "Genocide Denial Or Ideas Leading To It"),
]

created_count = 0
skipped = []

for key, label in REPORT_TYPES:
    obj, created = ReportType.objects.get_or_create(
        report_choice=key,
        defaults={"safe_to_auto_forward": False}
    )
    if created:
        created_count += 1
        print(f"✅ Created report type: {label} ({key})")
    else:
        skipped.append(key)

print(f"\n✅ Total created: {created_count}")
if skipped:
    print(f"⏭️ Already existing, skipped: {skipped}")
