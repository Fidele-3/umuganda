from django.urls import path
from users.views.api_views.citizen_register import RegisterUserAPIView
from users.views.api_views.citizen_login import citizenLoginView
from users.views.api_views.citizen_logout import citizenLogoutView
from users.views.api_views.dashboard_upload import DashboardMediaUploadView
from users.views.api_views.dashboard_list import DashboardMediaListView
from users.views.api_views.reset_password import RequestPasswordResetOTPView, ResetPasswordView, VerifyResetOTPView
from users.views.api_views.profile_view import UserProfileView
from users.views.api_views.settings import SettingsDashboardView
from users.views.views.admin_login import admin_login_view
from users.views.views.superadmin_dashboard_view import SuperAdminDashboardView
from users.views.views.super_admin_register import super_admin_register_view
from users.views.views.create_sector import create_sector_view
from users.views.views.create_level_2_admin import CreateAdminLevel2View
from users.views.views.adresses import get_cells, get_districts, get_sectors, get_villages
from users.views.views.view_admin_profile import view_admin_profile
from users.views.views.admin_edit_profile import edit_admin_profile
from users.views.views.request_otp_form import request_password_otp_view
from users.views.views.verify_otp import verify_reset_otp_view
from users.views.views.password_rest import final_password_reset_view 
from users.views.views.sector_officer_dashboard_view import AdminLevel2DashboardView 
from users.views.views.logout_view import LogoutView  
from users.views.views.create_level_3_admin import CreateAdminLevel3View
from users.views.views.cell_officer_dashboard import AdminLevel3DashboardView
from users.views.views.action_log_list_view import AdminActionLogListView
from users.views.views.umuganda_overview import SuperAdminUmugandaOverviewView
from umuganda.views.views.umuganda_session_sector import create_umuganda_session
from users.views.views.session_participants import SessionParticipantListView
from users.views.views.session_attendance import SessionAttendanceSubmitView
from umuganda.views.views.umuganda_session import CreateUmugandaSessionView
from umuganda.views.views.umuganda_session_detail import UmugandaSessionDetailView
from umuganda.views.views.umuganda_session_list import UmugandaSessionListView
from umuganda.views.views.umuganda_fines_list import UmugandaFinesListView
from umuganda.views.views.feedback_views import UmugandaFeedbackListView
from users.views.api_views.dashbord import CitizenDashboardView
from users.views.api_views.session_view import UmugandaSessionDetailViews
from users.views.api_views.fine_claim import ClaimFineAPIView
from users.views.api_views.fine_view import ListApplicableFinesAPIView
from users.views.views.sector_fines_overview import SectorFinesOverviewView
from users.views.views.umuganda_session_detail import umuganda_session_detail

urlpatterns = [
    path('citizen/register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('login/', citizenLoginView.as_view(), name='citizen_login'),
    path('logout/', citizenLogoutView.as_view(), name='citizen_logout'),
    path('dashboard/upload/', DashboardMediaUploadView.as_view(), name='user-dashboard-upload'),
    path('dashboard/media/', DashboardMediaListView.as_view(), name='user-dashboard-media'),
    path('reset-password/', RequestPasswordResetOTPView.as_view(), name='password-reset-otp'),
    path('reset-password/verify/', VerifyResetOTPView.as_view(), name='verify-reset-otp'),
    path('reset-password/reset/', ResetPasswordView.as_view(), name='reset-password-link'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('settings/', SettingsDashboardView.as_view(), name='user-settings'),
    path('admins/login/', admin_login_view, name='admin_login'),
    path('superadmin/dashboard/', SuperAdminDashboardView.as_view(), name='superadmin_dashboard'),
    path('admin/register/', super_admin_register_view, name='super_admin_register'),
    path('sector/create/', create_sector_view, name='create_sector'),
    path('admin/level2/create/', CreateAdminLevel2View.as_view(), name='create_sector_officer'),
    path('ajax/get-districts/', get_districts, name='get_districts'),
    path('ajax/get-sectors/', get_sectors, name='get_sectors'),
    path('ajax/get-cells/', get_cells, name='get_cells'),
    path('ajax/get-villages/', get_villages, name='get_villages'),
    path('admin/profile/', view_admin_profile, name='admin_profile'),
    path('admin/edit-profile/', edit_admin_profile, name='edit_admin_profile'),
    path('request-otp/', request_password_otp_view, name='request_otp_form'),
    path('verify-otp/', verify_reset_otp_view, name='verify-reset-otp'),
    path('password-reset/', final_password_reset_view, name='password-reset-final'),
    path('admin/dashboard', AdminLevel2DashboardView.as_view(), name='sector_officer_dashboard'),
    path('logout/admin/', LogoutView.as_view(), name='logout-admin'),
    path('admin/level3/create/', CreateAdminLevel3View.as_view(), name='create_cell_officer'),
    path('admin/level/dashboard/', AdminLevel3DashboardView.as_view(), name='cell_officer_dashboard'),
    path('admin/action-logs/', AdminActionLogListView.as_view(), name='admin_action_log_list'),
    path('superadmin/umuganda-overview/', SuperAdminUmugandaOverviewView.as_view(), name='superadmin_umuganda_overview'),
    path('umuganda/date/create/', create_umuganda_session, name='create_umuganda_session'),
    path('umuganda/session/<uuid:session_id>/participants/', SessionParticipantListView.as_view(), name='umuganda_participants_list'),
    path('umuganda/session/<uuid:session_id>/attendance/', SessionAttendanceSubmitView.as_view(), name='submit_session_attendance'),
    path('umuganda/session/create/', CreateUmugandaSessionView.as_view(), name='create_umuganda_session_view'),
    path('umuganda/session/<uuid:session_id>/', UmugandaSessionDetailView.as_view(), name='umuganda_session_detail'),
    path('umuganda/sessions/', UmugandaSessionListView.as_view(), name='umuganda_session_list'),
    path('umuganda/fines/<uuid:session_id>/', UmugandaFinesListView.as_view(), name='umuganda_fines_list'),
    path('umuganda/feedback/', UmugandaFeedbackListView.as_view(), name='umuganda_feedback_list'),
    path('citizen/dashboard/', CitizenDashboardView.as_view(), name='citizen_dashboard'),
    path('umuganda/session/<uuid:id>/detail/', UmugandaSessionDetailViews.as_view(), name='umuganda_citizen_session_detail'),
    path('umuganda/fines/claim/<uuid:fine_id>/claim', ClaimFineAPIView.as_view(), name='claim_fine'),
    path('umuganda/fines/list/', ListApplicableFinesAPIView.as_view(), name='list_applicable_fines'),
    path('sector/fines/overview/', SectorFinesOverviewView.as_view(), name='umuganda_fines_sector'),
    path('umuganda/sessions/<uuid:session_id>/detail/', umuganda_session_detail, name='umuganda_session_detail'),



]
