from decimal import Decimal

from rest_framework.test import APITestCase

from accounts.models import User
from recruiters.models import Company, Job, SkillTag
from students.models import Skill

from .models import Application

PASSWORD = 'TestPass123'


def make_recruiter(username, company):
    user = User.objects.create_user(username=username, password=PASSWORD, role='RECRUITER')
    profile = user.recruiter_profile  # created automatically by the signal
    profile.company = company
    profile.full_name = username
    profile.save()
    return user


def make_student(username, name, cgpa, skills, branch='IT'):
    user = User.objects.create_user(username=username, password=PASSWORD, role='STUDENT')
    profile = user.student_profile  # created automatically by the signal
    profile.full_name = name
    profile.branch = branch
    profile.cgpa = Decimal(cgpa)
    profile.graduation_year = 2027
    profile.save()
    for skill in skills:
        Skill.objects.create(student=profile, name=skill)
    return user


class ApplicationTestBase(APITestCase):
    """Shared data: two recruiters, one job (rec1's) and four students."""

    def setUp(self):
        company = Company.objects.create(name='Acme')
        python = SkillTag.objects.create(name='Python')
        django_tag = SkillTag.objects.create(name='Django')

        self.rec1 = make_recruiter('rec1', company)
        self.rec2 = make_recruiter('rec2', company)

        self.job = Job.objects.create(
            recruiter=self.rec1.recruiter_profile,
            title='Python Developer',
            description='Python and Django',
            min_cgpa=Decimal('7.0'),
            eligible_branches='CSE, IT',
        )
        self.job.required_skills.set([python, django_tag])

        self.stu1 = make_student('stu1', 'Student One', '8.5', ['Python', 'Django'])
        self.stu2 = make_student('stu2', 'Student Two', '8.0', ['Python'])
        self.stu3 = make_student('stu3', 'Student Three', '6.0', ['Python', 'Django'])
        self.stu4 = make_student('stu4', 'Student Four', '9.0', ['Python'])

    def apply(self, user):
        return Application.objects.create(student=user.student_profile, job=self.job)


class ApplyTests(ApplicationTestBase):
    def test_student_can_apply_once(self):
        self.client.force_authenticate(user=self.stu1)
        first = self.client.post('/api/applications/my/', {'job': self.job.id}, format='json')
        self.assertEqual(first.status_code, 201)
        second = self.client.post('/api/applications/my/', {'job': self.job.id}, format='json')
        self.assertEqual(second.status_code, 400)
        self.assertEqual(Application.objects.count(), 1)

    def test_student_cannot_choose_their_own_status(self):
        self.client.force_authenticate(user=self.stu1)
        response = self.client.post(
            '/api/applications/my/',
            {'job': self.job.id, 'status': 'SELECTED'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.get().status, 'APPLIED')

    def test_student_sees_only_their_own_applications(self):
        self.apply(self.stu1)
        self.apply(self.stu2)
        self.client.force_authenticate(user=self.stu1)
        response = self.client.get('/api/applications/my/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class RecruiterOwnershipTests(ApplicationTestBase):
    def test_recruiter_sees_applicants_only_for_own_job(self):
        self.apply(self.stu1)
        url = f'/api/applications/jobs/{self.job.id}/applicants/'

        self.client.force_authenticate(user=self.rec1)
        self.assertEqual(len(self.client.get(url).data), 1)

        self.client.force_authenticate(user=self.rec2)
        self.assertEqual(len(self.client.get(url).data), 0)

    def test_recruiter_can_only_update_status_for_own_jobs(self):
        application = self.apply(self.stu1)
        url = f'/api/applications/{application.id}/status/'

        self.client.force_authenticate(user=self.rec2)
        response = self.client.patch(url, {'status': 'SHORTLISTED'}, format='json')
        self.assertEqual(response.status_code, 404)
        application.refresh_from_db()
        self.assertEqual(application.status, 'APPLIED')

        self.client.force_authenticate(user=self.rec1)
        response = self.client.patch(url, {'status': 'SHORTLISTED'}, format='json')
        self.assertEqual(response.status_code, 200)
        application.refresh_from_db()
        self.assertEqual(application.status, 'SHORTLISTED')

    def test_invalid_status_is_rejected(self):
        application = self.apply(self.stu1)
        self.client.force_authenticate(user=self.rec1)
        response = self.client.patch(
            f'/api/applications/{application.id}/status/',
            {'status': 'HIRED'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)


class RankingTests(ApplicationTestBase):
    def test_ranking_puts_eligible_first_then_skill_match_then_cgpa(self):
        # stu1: 100% match, eligible        -> rank 1
        # stu4: 50% match, CGPA 9.0         -> rank 2 (wins the tie on CGPA)
        # stu2: 50% match, CGPA 8.0         -> rank 3
        # stu3: 100% match but CGPA 6.0     -> not eligible, so last
        for user in (self.stu1, self.stu2, self.stu3, self.stu4):
            self.apply(user)

        self.client.force_authenticate(user=self.rec1)
        response = self.client.get(f'/api/matching/jobs/{self.job.id}/report/')

        self.assertEqual(response.status_code, 200)
        names = [row['student_name'] for row in response.data]
        self.assertEqual(
            names, ['Student One', 'Student Four', 'Student Two', 'Student Three']
        )
        self.assertEqual([row['rank'] for row in response.data], [1, 2, 3, 4])
        self.assertFalse(response.data[3]['overall_eligible'])