from rest_framework.test import APITestCase

from .models import User

PASSWORD = 'TestPass123'


def make_user(username, role):
    return User.objects.create_user(username=username, password=PASSWORD, role=role)


class LoginTests(APITestCase):
    def setUp(self):
        make_user('stu', 'STUDENT')

    def test_login_returns_tokens(self):
        response = self.client.post(
            '/api/token/', {'username': 'stu', 'password': PASSWORD}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_wrong_password_is_refused(self):
        response = self.client.post(
            '/api/token/', {'username': 'stu', 'password': 'wrong'}, format='json'
        )
        self.assertEqual(response.status_code, 401)


class RegistrationTests(APITestCase):
    def register(self, username, role):
        return self.client.post(
            '/api/register/',
            {
                'username': username,
                'email': f'{username}@example.com',
                'password': PASSWORD,
                'role': role,
            },
            format='json',
        )

    def test_student_can_register_and_gets_a_profile(self):
        response = self.register('newstudent', 'STUDENT')
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='newstudent')
        self.assertEqual(user.role, 'STUDENT')
        self.assertTrue(hasattr(user, 'student_profile'))

    def test_recruiter_can_register_and_gets_a_profile(self):
        response = self.register('newrecruiter', 'RECRUITER')
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='newrecruiter')
        self.assertTrue(hasattr(user, 'recruiter_profile'))

    def test_cannot_register_as_admin_or_tpo(self):
        for role in ('ADMIN', 'TPO'):
            with self.subTest(role=role):
                response = self.register(f'sneaky_{role}', role)
                self.assertEqual(response.status_code, 400)
                self.assertFalse(User.objects.filter(username=f'sneaky_{role}').exists())


class RolePermissionTests(APITestCase):
    def setUp(self):
        self.student = make_user('stu', 'STUDENT')
        self.recruiter = make_user('rec', 'RECRUITER')
        self.tpo = make_user('tpo', 'TPO')

    def call(self, method, url):
        if method == 'get':
            return self.client.get(url)
        return getattr(self.client, method)(url, {}, format='json')

    def test_anonymous_requests_are_refused(self):
        urls = [
            '/api/me/',
            '/api/tpo/stats/',
            '/api/student/profile/',
            '/api/recruiter/my-jobs/',
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 401)

    def test_student_is_refused_on_recruiter_and_tpo_endpoints(self):
        self.client.force_authenticate(user=self.student)
        cases = [
            ('get', '/api/tpo/stats/'),
            ('get', '/api/recruiter/my-jobs/'),
            ('get', '/api/recruiter/profile/'),
            ('post', '/api/recruiter/skills/'),
            ('get', '/api/matching/jobs/1/report/'),
            ('get', '/api/applications/jobs/1/applicants/'),
            ('patch', '/api/applications/1/status/'),
        ]
        for method, url in cases:
            with self.subTest(method=method, url=url):
                self.assertEqual(self.call(method, url).status_code, 403)

    def test_recruiter_is_refused_on_student_and_tpo_endpoints(self):
        self.client.force_authenticate(user=self.recruiter)
        urls = [
            '/api/tpo/stats/',
            '/api/student/profile/',
            '/api/student/skills/',
            '/api/student/education/',
            '/api/applications/my/',
            '/api/prediction/jobs/1/my-chance/',
            '/api/matching/jobs/1/skill-gap/',
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

    def test_tpo_can_read_stats(self):
        self.client.force_authenticate(user=self.tpo)
        response = self.client.get('/api/tpo/stats/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['totals']['students'], 1)
        self.assertEqual(response.data['totals']['recruiters'], 1)

    def test_me_returns_the_role(self):
        self.client.force_authenticate(user=self.recruiter)
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'RECRUITER')