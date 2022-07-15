from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from base.models import Students, Subjects, CustomUser, Attendance, AttendanceReport, LeaveReportStudent, \
    FeedBackStudent, Courses, SessionYearModel, StudentResult


def student_home(request):
    return render(request, "student_template/student_home_template.html")


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
                                                                attendance_id__subject_id=subject_id)
    return render(request, "student_template/student_view_attendance.html",
                  {'subjects': subjects, 'action': action, 'get_subject': get_subject,
                   'attendance_report': attendance_report})


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    total = None
    for i in student_result:
        assignment_marks = i.subject_assignment_marks
        exam_marks = i.subject_exam_marks
        total = assignment_marks + exam_marks

    return render(request, "student_template/student_view_result.html",
                  {"student_result": student_result, 'total': total})


def student_apply_leave(request):
    staff_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=staff_obj)
    return render(request, "student_template/student_apply_leave.html", {"leave_data": leave_data})


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
        except messages as ex:
            ex.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    staff_id = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=staff_id)
    return render(request, "student_template/student_feedback.html", {"feedback_data": feedback_data})


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
        except messages as ex:
            ex.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    return render(request, "student_template/student_profile.html", {"user": user, "student": student})


def student_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        address = request.POST.get("address")
        print(profile_pic)
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password is not None and password != "":
                customuser.set_password(password)
            if profile_pic is not None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()

            student = Students.objects.get(admin=customuser)
            student.address = address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))