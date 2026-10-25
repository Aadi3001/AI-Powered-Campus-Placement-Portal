from rest_framework.test import APITestCase

from accounts.models import User

from .models import Company, Job, SkillTag

PASSWORD = 'TestPass123'


class JobPostingTests(APITestCase):
    def setUp(self):
        SkillTag.objects.create(name='Python')
        SkillTag.objects.create(name='Django')
        self.user = User.objects.create_user(
            username='rec', password=PASSWORD, role='RECRUITER'
        )
        self.profile = self.user.recruiter_profile  # created by the signal
        self.client.force_authenticate(user=self.user)

    def give_company(self):
        self.profile.company = Company.objects.create(name='Acme')
        self.profile.save()

    def post_job(self, **extra):
        payload = {
            'title': 'Backend Developer',
            'description': 'We need Python and Django experience.',
            'eligible_branches': 'CSE, IT',
        }
        payload.update(extra)
        return self.client.post('/api/recruiter/jobs/', payload, format='json')

    def skill_names(self):
        job = Job.objects.get()
        return sorted(job.required_skills.values_list('name', flat=True))

    def test_company_is_required_before_posting(self):
        response = self.post_job()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Job.objects.count(), 0)

    def test_skills_are_detected_from_the_description(self):
        self.give_company()
        response = self.post_job()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.skill_names(), ['Django', 'Python'])

    def test_explicit_skills_override_detection(self):
        self.give_company()
        django_tag = SkillTag.objects.get(name='Django')
        response = self.post_job(required_skills=[django_tag.id])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.skill_names(), ['Django'])

    def test_invalid_branch_code_is_rejected(self):
        self.give_company()
        response = self.post_job(eligible_branches='CSE, NOPE')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Job.objects.count(), 0)

    def test_student_cannot_post_a_job(self):
        student = User.objects.create_user(
            username='stu', password=PASSWORD, role='STUDENT'
        )
        self.client.force_authenticate(user=student)
        self.assertEqual(self.post_job().status_code, 403)