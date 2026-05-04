from django.test import TestCase, Client
from django.urls import reverse

from base.models import CustomUser, Courses, SessionYearModel, Staffs, Students


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='admin', password='testpass123', email='admin@test.com', user_type="1"
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse('show_login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('do_login'), {
            'email': 'admin@test.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_failure(self):
        response = self.client.post(reverse('do_login'), {
            'email': 'admin@test.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_login_get_not_allowed(self):
        response = self.client.get(reverse('do_login'))
        self.assertEqual(response.status_code, 405)


class AuthorizationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.hod = CustomUser.objects.create_user(
            username='hod', password='testpass123', email='hod@test.com', user_type="1"
        )
        self.staff_user = CustomUser.objects.create_user(
            username='staff', password='testpass123', email='staff@test.com', user_type="2"
        )
        self.student_user = CustomUser.objects.create_user(
            username='student', password='testpass123', email='student@test.com', user_type="3"
        )

    def test_unauthenticated_redirect_to_login(self):
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 302)

    def test_staff_cannot_access_admin_views(self):
        self.client.login(username='staff', password='testpass123')
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 302)

    def test_student_cannot_access_admin_views(self):
        self.client.login(username='student', password='testpass123')
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 302)


class DeleteRequiresPostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.hod = CustomUser.objects.create_user(
            username='hod', password='testpass123', email='hod@test.com', user_type="1"
        )
        self.client.login(username='hod', password='testpass123')
        self.course = Courses.objects.create(course_name="Test Course")

    def test_delete_course_get_not_allowed(self):
        response = self.client.get(
            reverse('delete_course', kwargs={'course_id': self.course.id})
        )
        self.assertEqual(response.status_code, 405)

    def test_delete_course_post_works(self):
        response = self.client.post(
            reverse('delete_course', kwargs={'course_id': self.course.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Courses.objects.filter(id=self.course.id).exists())


class ModelTestCase(TestCase):
    def test_course_str(self):
        course = Courses.objects.create(course_name="Computer Science")
        self.assertEqual(str(course), "Computer Science")

    def test_session_year_str(self):
        sy = SessionYearModel.objects.create(
            session_start_year="2024", session_end_year="2025"
        )
        self.assertEqual(str(sy), "2024 to 2025")

    def test_user_profile_auto_created_hod(self):
        user = CustomUser.objects.create_user(
            username='hod2', password='test', email='hod2@test.com', user_type="1"
        )
        self.assertTrue(hasattr(user, 'adminhod'))

    def test_user_profile_auto_created_staff(self):
        user = CustomUser.objects.create_user(
            username='staff2', password='test', email='staff2@test.com', user_type="2"
        )
        self.assertTrue(hasattr(user, 'staffs'))

    def test_user_profile_auto_created_student(self):
        user = CustomUser.objects.create_user(
            username='student2', password='test', email='student2@test.com', user_type="3"
        )
        self.assertTrue(hasattr(user, 'students'))
