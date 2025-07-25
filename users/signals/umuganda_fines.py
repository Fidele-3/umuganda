from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile
from umuganda.models import UmugandaSession, Attendance, Fine

@receiver(post_save, sender=UmugandaSession)
def assign_fines_to_absentees(sender, instance: UmugandaSession, created, **kwargs):
    if created:
        return  # Don't process on session creation

    # Ensure the session date has passed
    if instance.date >= now().date():
        return  # Don't process future sessions

    # Get all relevant citizens based on scope (village > cell > sector)
    users = CustomUser.objects.filter(user_level='citizen', is_active=True)

    if instance.village:
        users = users.filter(profile__village=instance.village)
    elif instance.cell:
        users = users.filter(profile__cell=instance.cell)
    else:
        users = users.filter(profile__sector=instance.sector)

    for user in users:
        # Check if the user was already marked present
        attendance_exists = Attendance.objects.filter(
            user=user,
            session=instance,
            status='present'
        ).exists()

        if attendance_exists:
            continue  # Already marked present — no fine needed

        # Create an absent attendance if none exists
        Attendance.objects.get_or_create(
            user=user,
            session=instance,
            defaults={
                'status': 'absent',
                'remarks': 'Automatically marked absent by system',
            }
        )

        # Avoid duplicate fine
        Fine.objects.get_or_create(
            user=user,
            session=instance,
            defaults={
                'amount': instance.fines_policy,
                'reason': 'Absent from Umuganda session',
            }
        )
