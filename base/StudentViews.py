import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from base.decorators import student_required
from base.models import Students, Subjects, CustomUser, Attendance, AttendanceReport, LeaveReportStudent, \
    FeedBackStudent, Courses, SessionYearModel, StudentResult

logger = logging.getLogger(__name__)


@student_required
def student_home(request):
    student_obj = Students.objects.select_related('course_id', 'session_year_id').get(admin=request.user.id)
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj).count()
    course_subjects = Subjects.objects.filter(course_id=student_obj.course_id)
    attendance_total = Attendance.objects.filter(
        subject_id__in=course_subjects,
        session_year_id=student_obj.session_year_id
    ).count()
    attendance_absent = attendance_total - attendance_present
    subjects = course_subjects.count()

    return render(request, "student_template/student_home_template.html",
                  {'attendance_total': attendance_total, 'attendance_present': attendance_present,
                   'attendance_absent': attendance_absent, 'subjects': subjects})


@student_required
def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "student_template/student_profile.html", {"user": user})


@student_required
def student_profile_save(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password is not None and password != "":
                customuser.set_password(password)
            if profile_pic is not None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except Exception:
            logger.exception("Failed to update student profile")
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))


@student_required
def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    subjects = Subjects.objects.filter(course_id=student.course_id)

    action = request.GET.get('action')
    get_subject = None
    attendance_report = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subjects.objects.get(id=subject_id)

            attendance_report = AttendanceReport.objects.filter(student_id=student,
                                                                attendance_id__subject_id=subject_id).select_related('attendance_id')
    return render(request, "student_template/student_view_attendance.html",
                  {'subjects': subjects, 'action': action, 'get_subject': get_subject,
                   'attendance_report': attendance_report})


@student_required
def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id).select_related('subject_id')
    total = sum(r.subject_assignment_marks + r.subject_exam_marks for r in student_result)

    return render(request, "student_template/student_view_result.html",
                  {"student_result": student_result, 'total': total})


@student_required
def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request, "student_template/student_apply_leave.html", {"leave_data": leave_data})


@student_required
def student_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_msg,
                                              leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except Exception:
            logger.exception("Failed to apply for student leave")
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


@student_required
def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    return render(request, "student_template/student_feedback.html", {"feedback_data": feedback_data})


@student_required
def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackStudent(student_id=student_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except Exception:
            logger.exception("Failed to send student feedback")
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
