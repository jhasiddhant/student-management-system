from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from base import views, HodViews, StaffViews, StudentViews
from student_management_system import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('doLogin', views.doLogin, name="do_login"),
                  path('', views.ShowLoginPage, name="show_login"),
                  path('get_user_details', views.GetUserDetails),
                  path('logout_user', views.logout_user, name="logout"),

                  # Admin
                  path('admin_home', HodViews.admin_home, name="admin_home"),
                  path('admin_profile', HodViews.admin_profile, name="admin_profile"),
                  path('admin_profile_save', HodViews.admin_profile_save, name="admin_profile_save"),

                  path('add_staff', HodViews.add_staff, name="add_staff"),
                  path('add_staff_save', HodViews.add_staff_save, name="add_staff_save"),
                  path('manage_staff', HodViews.manage_staff, name="manage_staff"),
                  path('edit_staff/<str:staff_id>', HodViews.edit_staff, name="edit_staff"),
                  path('edit_staff_save', HodViews.edit_staff_save, name="edit_staff_save"),
                  path('delete_staff/<str:staff_id>/', HodViews.delete_staff, name="delete_staff"),

                  path('add_course', HodViews.add_course, name="add_course"),
                  path('add_course_save', HodViews.add_course_save, name="add_course_save"),
                  path('manage_course', HodViews.manage_course, name="manage_course"),
                  path('edit_course/<str:course_id>', HodViews.edit_course, name="edit_course"),
                  path('edit_course_save', HodViews.edit_course_save, name="edit_course_save"),
                  path('delete_course/<course_id>/', HodViews.delete_course, name="delete_course"),

                  path('add_subject', HodViews.add_subject, name="add_subject"),
                  path('add_subject_save', HodViews.add_subject_save, name="add_subject_save"),
                  path('manage_subject', HodViews.manage_subject, name="manage_subject"),
                  path('edit_subject/<str:subject_id>', HodViews.edit_subject, name="edit_subject"),
                  path('edit_subject_save', HodViews.edit_subject_save, name="edit_subject_save"),
                  path('delete_subject/<str:subject_id>/', HodViews.delete_subject, name="delete_subject"),

                  path('add_session', HodViews.add_session, name="add_session"),
                  path('manage_session', HodViews.manage_session, name="manage_session"),
                  path('add_session_save/', HodViews.add_session_save, name="add_session_save"),
                  path('edit_session/<str:session_id>', HodViews.edit_session, name="edit_session"),
                  path('edit_session_save/', HodViews.edit_session_save, name="edit_session_save"),
                  path('delete_session/<str:session_id>/', HodViews.delete_session, name="delete_session"),

                  path('add_student', HodViews.add_student, name="add_student"),
                  path('add_student_save', HodViews.add_student_save, name="add_student_save"),
                  path('manage_student', HodViews.manage_student, name="manage_student"),
                  path('edit_student/<str:student_id>', HodViews.edit_student, name="edit_student"),
                  path('edit_student_save', HodViews.edit_student_save, name="edit_student_save"),
                  path('delete_student/<str:student_id>/', HodViews.delete_student, name="delete_student"),

                  path('staff_leave_view', HodViews.staff_leave_view, name="staff_leave_view"),
                  path('staff_disapprove_leave/<str:leave_id>', HodViews.staff_disapprove_leave,
                       name="staff_disapprove_leave"),
                  path('staff_approve_leave/<str:leave_id>', HodViews.staff_approve_leave, name="staff_approve_leave"),

                  path('student_leave_view', HodViews.student_leave_view, name="student_leave_view"),
                  path('student_approve_leave/<str:leave_id>', HodViews.student_approve_leave,
                       name="student_approve_leave"),
                  path('student_disapprove_leave/<str:leave_id>', HodViews.student_disapprove_leave,
                       name="student_disapprove_leave"),

                  path('staff_feedback_message', HodViews.staff_feedback_message, name="staff_feedback_message"),
                  path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied,
                       name="staff_feedback_message_replied"),

                  path('student_feedback_message', HodViews.student_feedback_message, name="student_feedback_message"),
                  path('student_feedback_message_replied', HodViews.student_feedback_message_replied,
                       name="student_feedback_message_replied"),

                  path('admin_view_attendance', HodViews.admin_view_attendance, name="admin_view_attendance"),


                  # Staff
                  path('staff_home', StaffViews.staff_home, name="staff_home"),
                  path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
                  path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),

                  path('staff_take_attendance', StaffViews.staff_take_attendance, name="staff_take_attendance"),
                  path('save_attendance_data', StaffViews.save_attendance_data, name="save_attendance_data"),
                  path('view_attendance_data', StaffViews.view_attendance_data, name="view_attendance_data"),

                  path('staff_add_results', StaffViews.staff_add_results, name="staff_add_results"),
                  path('staff_save_results', StaffViews.staff_save_results, name="staff_save_results"),

                  path('staff_apply_leave', StaffViews.staff_apply_leave, name="staff_apply_leave"),
                  path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),

                  path('staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
                  path('staff_feedback_save', StaffViews.staff_feedback_save, name="staff_feedback_save"),

                  # Student
                  path('student_home', StudentViews.student_home, name="student_home"),
                  path('student_profile', StudentViews.student_profile, name="student_profile"),
                  path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),

                  path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),

                  path('student_view_result', StudentViews.student_view_result, name="student_view_result"),

                  path('student_apply_leave', StudentViews.student_apply_leave, name="student_apply_leave"),
                  path('student_apply_leave_save', StudentViews.student_apply_leave_save,
                       name="student_apply_leave_save"),

                  path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
                  path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.
                                                                                         STATIC_ROOT)
