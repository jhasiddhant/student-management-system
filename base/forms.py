from django import forms
from django.core.validators import FileExtensionValidator
from base.models import Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


def validate_image_size(file):
    max_size = 2 * 1024 * 1024  # 2MB
    if file.size > max_size:
        raise forms.ValidationError("Image file size must be under 2MB.")


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    course = forms.ChoiceField(label="Course", choices=[],
                               widget=forms.Select(attrs={"class": "form-control"}))
    sex = forms.ChoiceField(label="Sex", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=[],
                                        widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.ImageField(label="Profile Pic", required=False,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
                                       validate_image_size,
                                   ],
                                   widget=forms.FileInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].choices = [
            (c.id, c.course_name) for c in Courses.objects.all()
        ]
        self.fields['session_year_id'].choices = [
            (s.id, f"{s.session_start_year} to {s.session_end_year}")
            for s in SessionYearModel.objects.all()
        ]


class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    course = forms.ChoiceField(label="Course", choices=[],
                               widget=forms.Select(attrs={"class": "form-control"}))
    sex = forms.ChoiceField(label="Sex", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=[],
                                        widget=forms.Select(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].choices = [
            (c.id, c.course_name) for c in Courses.objects.all()
        ]
        self.fields['session_year_id'].choices = [
            (s.id, f"{s.session_start_year} to {s.session_end_year}")
            for s in SessionYearModel.objects.all()
        ]