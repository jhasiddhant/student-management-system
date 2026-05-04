from django.urls import path

from base import StudentViews

urlpatterns = [
    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),

    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),

    path('student_view_result', StudentViews.student_view_result, name="student_view_result"),

    path('student_apply_leave', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),

    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),
]
