from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile
from umuganda.models import CellUmugandaSession, Attendance, Fine

@receiver(post_save, sender=CellUmugandaSession)
def assign_fines_to_absentees(sender, instance: CellUmugandaSession, created, **kwargs):
  
    if instance.sector_session.date >= now().date():
        return

   
    users = CustomUser.objects.filter(user_level='citizen', is_active=True)

    if instance.village:
        users = users.filter(profile__village=instance.village)
    else:
        users = users.filter(profile__cell=instance.cell)

    for user in users:
       
        attendance_exists = Attendance.objects.filter(
            user=user,
            session=instance,
            status='present'
        ).exists()

        if attendance_exists:
            continue  
       
        Attendance.objects.get_or_create(
            user=user,
            session=instance,
            defaults={
                'status': 'absent',
                'remarks': 'Automatically marked absent by system',
            }
        )

        # Issue fine if not already fined
        if instance.fines_policy:
            Fine.objects.get_or_create(
                user=user,
                session=instance,
                defaults={
                    'amount': instance.fines_policy,
                    'reason': 'Absent from Umuganda session',
                }
            )
