import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from datetime import datetime, timezone as Time

from umuganda.models import Fine, Attendance, UmugandaSession
from users.serializer.fine_serializer import FineSerializer

logger = logging.getLogger(__name__)


class ListApplicableFinesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()

        # Access UserProfile related to user
        user_profile = getattr(user, "profile", None)
        if not user_profile:
            logger.error("User profile not found for user ID %s", user.id)
            return Response({"detail": "User profile not found."}, status=400)

        user_cell = getattr(user_profile, "cell", None)
        user_sector = getattr(user_cell, "sector", None) if user_cell else None

        if not user_cell or not user_sector:
            logger.error("User cell or sector not set in profile for user ID %s", user.id)
            return Response({"detail": "User cell or sector not set in profile."}, status=400)

        try:
            # Filter sessions and fines with correct cell and sector
            all_sessions = UmugandaSession.objects.filter(cell=user_cell, cell__sector=user_sector)

            existing_fines = Fine.objects.filter(
                user=user,
                session__cell=user_cell,
                session__cell__sector=user_sector
            ).exclude(
                Q(status='paid', paid_at__isnull=False, payment_id__isnull=False) |
                Q(claim=True, claim_has_been_approved=True)
            )
            logger.info(f"Found {existing_fines.count()} existing unpaid/unclaimed fines for user {user.id}.")
        except Exception as e:
            logger.exception("Failed to fetch existing fines.")
            return Response({"detail": "Error loading fines."}, status=500)

        applicable_fines = []

        # Add/Update real existing fines
        for fine in existing_fines:
            logger.debug(f"Processing existing fine ID: {fine.id}")
            try:
                issued_at = fine.issued_at
                if not isinstance(issued_at, datetime):
                    issued_at = datetime.combine(issued_at, datetime.min.time(), tzinfo=Time.utc)

                months_passed = relativedelta(now, issued_at).months + (12 * (now.year - issued_at.year))
                if months_passed > fine.moths_overdue:
                    fine.moths_overdue = months_passed
                    fine.save(update_fields=['moths_overdue'])
                    logger.info(f"Updated overdue months for fine ID {fine.id} to {months_passed}")

                if fine.session and fine.session.fines_policy != fine.amount:
                    fine.amount = fine.session.fines_policy
                    fine.save(update_fields=['amount'])
                    logger.info(f"Updated fine amount for fine ID {fine.id} to match session policy")

                applicable_fines.append(fine)
            except Exception as e:
                logger.exception(f"Error processing fine ID: {fine.id}")

        try:
            session_ids_with_fines = existing_fines.values_list('session_id', flat=True)
            attendance_sessions = Attendance.objects.filter(user=user).values_list('session_id', flat=True)
            logger.info(f"User has attendance in {len(attendance_sessions)} sessions.")
        except Exception as e:
            logger.exception("Failed to fetch attendance or fined sessions.")
            return Response({"detail": "Error loading attendance data."}, status=500)

        for session in all_sessions:
            if session.id in attendance_sessions:
                logger.debug(f"Skipping session {session.id} (attended)")
                continue
            if session.id in session_ids_with_fines:
                logger.debug(f"Skipping session {session.id} (already fined)")
                continue

            try:
                fines_policy_value = float(session.fines_policy)
            except (ValueError, TypeError):
                fines_policy_value = 0.0  # treat invalid as zero

            if fines_policy_value <= 0:
                logger.debug(f"Skipping session {session.id} because fines_policy is not set or zero.")
                continue

            if session.date > now.date():
                logger.debug(f"Skipping session {session.id} because session date {session.date} is in the future.")
                continue

    


            try:
                session_date = session.date
                if not isinstance(session_date, datetime):
                    session_date = datetime.combine(session_date, datetime.min.time(), tzinfo=Time.utc)

                months_overdue = relativedelta(now, session_date).months + (12 * (now.year - session_date.year))

                virtual_fine = Fine(
                    id=None,
                    user=user,
                    session=session,
                    amount=session.fines_policy,
                    status='unpaid',
                    moths_overdue=months_overdue,
                    issued_at=session_date,
                    paid_at=None,
                    payment_method=None,
                    payment_id=None,
                    reason=None,
                    claim=False,
                    claim_has_been_approved=False
                )
                logger.info(f"Generated virtual fine for session {session.id}, overdue {months_overdue} months.")
                applicable_fines.append(virtual_fine)
            except Exception as e:
                logger.exception(f"Failed to generate virtual fine for session {session.id}")

        try:
            serializer = FineSerializer(applicable_fines, many=True)
            logger.info("Successfully serialized applicable fines.")
            return Response({
                "has_fines": len(applicable_fines) > 0,
                "fines": serializer.data
            })
        except Exception as e:
            logger.exception("Failed to serialize fines.")
            return Response({"detail": "Error serializing fines."}, status=500)
