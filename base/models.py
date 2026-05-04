import logging

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


class LeaveStatus(models.IntegerChoices):
    PENDING = 0, "Pending"
    APPROVED = 1, "Approved"
    DISAPPROVED = 2, "Disapproved"


class GenderChoices(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"


class SessionYearModel(models.Model):
    session_start_year = models.CharField(max_length=100)
    session_end_year = models.CharField(max_length=100)

    def __str__(self):
        return self.session_start_year + " to " + self.session_end_year


class CustomUser(AbstractUser):
    user_type_data = (("1", "HOD"), ("2", "Staff"), ("3", "Student"))
    user_type = models.CharField(default="1", choices=user_type_data, max_length=10)
    profile_pic = models.ImageField(upload_to='profiles', default='avatar.svg')


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_type = str(instance.user_type)
        try:
            if user_type == "1":
                AdminHOD.objects.create(admin=instance)
            elif user_type == "2":
                Staffs.objects.create(admin=instance, address="")
            elif user_type == "3":
                Students.objects.create(admin=instance, address="", gender="")
        except Exception:
            logger.exception("Failed to create profile for user %s", instance.username)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    user_type = str(instance.user_type)
    try:
        if user_type == "1" and hasattr(instance, 'adminhod'):
            instance.adminhod.save()
        elif user_type == "2" and hasattr(instance, 'staffs'):
            instance.staffs.save()
        elif user_type == "3" and hasattr(instance, 'students'):
            instance.students.save()
    except Exception:
        logger.exception("Failed to save profile for user %s", instance.username)


class AdminHOD(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Staffs(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username


class Courses(models.Model):
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name


class Subjects(models.Model):
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1, related_name='subjects')
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subjects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name


class Students(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, blank=True, default="")
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.PROTECT, null=True, blank=True, related_name='students')
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.PROTECT, null=True, blank=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username


class Attendance(models.Model):
    subject_id = models.ForeignKey(Subjects, on_delete=models.PROTECT, related_name='attendances')
    attendance_date = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.PROTECT, related_name='attendances')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_id.subject_name


class AttendanceReport(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='attendance_reports')
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student_id', 'attendance_id'], name='unique_attendance_report')
        ]

    def __str__(self):
        return self.student_id.admin.username


class LeaveReportStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='leave_reports')
    leave_date = models.DateField()
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=LeaveStatus.PENDING, choices=LeaveStatus.choices, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name='leave_reports')
    leave_date = models.DateField()
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=LeaveStatus.PENDING, choices=LeaveStatus.choices, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='feedbacks')
    feedback = models.TextField()
    feedback_reply = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackStaffs(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name='feedbacks')
    feedback = models.TextField()
    feedback_reply = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentResult(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='results')
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='results')
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student_id', 'subject_id'], name='unique_student_result')
        ]

    def __str__(self):
        return self.student_id.admin.username
