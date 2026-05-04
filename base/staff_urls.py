from django.urls import path

from base import StaffViews

urlpatterns = [
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
]
