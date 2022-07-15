import json

from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from base.models import SessionYearModel, Subjects, Students, Attendance, AttendanceReport, Staffs, FeedBackStaffs, \
    LeaveReportStaff, CustomUser, StudentResult


def staff_home(request):
    return render(request, "staff_template/staff_home_template.html", )


def staff_take_attendance(request):
    subject = Subjects.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_sessionYear = None
    students = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subjects.objects.get(id=subject_id)
            get_sessionYear = SessionYearModel.objects.get(id=session_year_id)

            subject = Subjects.objects.filter(id=subject_id)

            for i in subject:
                student_id = i.course_id.id
                students = Students.objects.filter(course_id=student_id)

    return render(request, "staff_template/staff_take_attendance.html",
                  {'subject': subject, 'session_year': session_year, 'get_subject': get_subject,
                   'get_sessionYear': get_sessionYear, 'action': action, 'students': students})


def save_attendance_data(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_ids = request.POST.get('student_ids')

        get_subject = Subjects.objects.get(id=subject_id)
        get_sessionYear = SessionYearModel.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id=get_subject,
            attendance_date=attendance_date,
            session_year_id=get_sessionYear
        )
        attendance.save()

        for stud in student_ids:
            stud_id = stud
            int_stud = int(stud_id)
            p_students = Students.objects.get(id=int_stud)
            attendance_report = AttendanceReport(
                student_id=p_students,
                attendance_id=attendance
            )
            attendance_report.save()

    return redirect('staff_take_attendance')


def view_attendance_data(request):
    subject = Subjects.objects.filter(staff_id=request.user.id)
    session_year = SessionYearModel.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_sessionYear = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subjects.objects.get(id=subject_id)
            get_sessionYear = SessionYearModel.objects.get(id=session_year_id)
            attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = AttendanceReport.objects.filter(
                    attendance_id=attendance_id)

    return render(request, 'staff_template/staff_view_attendance.html',
                  {'subject': subject, 'session_year': session_year, 'action': action, 'get_subject': get_subject,
                   'get_sessionYear': get_sessionYear, 'attendance_date': attendance_date,
                   'attendance_report': attendance_report})


def staff_add_results(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_sessionYear = None
    students = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subjects.objects.get(id=subject_id)
            get_sessionYear = SessionYearModel.objects.get(id=session_year_id)

            subjects = Subjects.objects.filter(id=subject_id)
            for i in subjects:
                student_id = i.course_id.id
                students = Students.objects.filter(course_id=student_id)

    return render(request, "staff_template/staff_add_result.html",
                  {"subjects": subjects, "session_years": session_years, 'action': action,
                   'get_subject': get_subject, 'get_sessionYear': get_sessionYear, 'students': students})


def staff_save_results(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')

        get_student = Students.objects.get(admin=student_id)
        get_subject = Subjects.objects.get(id=subject_id)

        check_exist = StudentResult.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=get_subject, student_id=get_student)
            result.subject_assignment_marks = assignment_marks
            result.subject_exam_marks = exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("staff_add_results"))
        else:
            result = StudentResult(student_id=get_student, subject_id=get_subject, subject_exam_marks=exam_marks,
                                   subject_assignment_marks=assignment_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("staff_add_results"))


def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request, "staff_template/staff_apply_leave.html", {"leave_data": leave_data})


def staff_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_msg,
                                            leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except messages as ex:
            ex.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))


def staff_feedback(request):
    staff_id = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request, "staff_template/staff_feedback.html", {"feedback_data": feedback_data})


def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except messages as ex:
            ex.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)
    return render(request, "staff_template/staff_profile.html", {"user": user, "staff": staff})


def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password is not None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))


