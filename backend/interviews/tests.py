from datetime import timedelta

from django.utils import timezone

from applications.tests import ApplicationTestBase
from notifications.models import Notification

from .models import Interview


class InterviewTests(ApplicationTestBase):
    def setUp(self):
        super().setUp()
        self.application = self.apply(self.stu1)
        self.application.status = 'SHORTLISTED'
        self.application.save()
        self.in_two_days = (timezone.now() + timedelta(days=2)).isoformat()

    def schedule(self, user, **overrides):
        self.client.force_authenticate(user=user)
        payload = {
            'application': self.application.id,
            'round_name': 'Technical',
            'scheduled_at': self.in_two_days,
            'mode': 'ONLINE',
            'location_or_link': 'https://meet.example.com/abc',
        }
        payload.update(overrides)
        return self.client.post('/api/interviews/schedule/', payload, format='json')

    def make_interview(self, application=None):
        return Interview.objects.create(
            application=application or self.application,
            round_name='Technical',
            scheduled_at=timezone.now() + timedelta(days=2),
        )

    def test_recruiter_can_schedule_for_a_shortlisted_applicant(self):
        response = self.schedule(self.rec1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Interview.objects.count(), 1)
        notes = Notification.objects.filter(user=self.stu1)
        self.assertEqual(notes.count(), 1)
        self.assertIn('Technical', notes.get().message)

    def test_cannot_schedule_unless_shortlisted(self):
        self.application.status = 'APPLIED'
        self.application.save()
        response = self.schedule(self.rec1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Interview.objects.count(), 0)

    def test_other_recruiter_cannot_schedule(self):
        response = self.schedule(self.rec2)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Interview.objects.count(), 0)

    def test_cannot_schedule_in_the_past(self):
        past = (timezone.now() - timedelta(days=1)).isoformat()
        response = self.schedule(self.rec1, scheduled_at=past)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Interview.objects.count(), 0)

    def test_student_cannot_schedule(self):
        response = self.schedule(self.stu1)
        self.assertEqual(response.status_code, 403)

    def test_student_sees_only_their_own_interviews(self):
        other = self.apply(self.stu2)
        self.make_interview()
        self.make_interview(other)
        self.client.force_authenticate(user=self.stu1)
        response = self.client.get('/api/interviews/my/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['job_title'], 'Python Developer')

    def test_recruiter_sees_interviews_for_own_job_only(self):
        self.make_interview()
        url = f'/api/interviews/jobs/{self.job.id}/'
        self.client.force_authenticate(user=self.rec1)
        self.assertEqual(len(self.client.get(url).data), 1)
        self.client.force_authenticate(user=self.rec2)
        self.assertEqual(len(self.client.get(url).data), 0)

    def test_cancelling_notifies_the_student(self):
        interview = self.make_interview()
        self.client.force_authenticate(user=self.rec1)
        response = self.client.patch(
            f'/api/interviews/{interview.id}/', {'status': 'CANCELLED'}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        interview.refresh_from_db()
        self.assertEqual(interview.status, 'CANCELLED')
        notes = Notification.objects.filter(user=self.stu1)
        self.assertEqual(notes.count(), 1)
        self.assertIn('cancelled', notes.get().message.lower())

    def test_other_recruiter_cannot_update_an_interview(self):
        interview = self.make_interview()
        self.client.force_authenticate(user=self.rec2)
        response = self.client.patch(
            f'/api/interviews/{interview.id}/', {'status': 'CANCELLED'}, format='json'
        )
        self.assertEqual(response.status_code, 404)

    def test_rescheduling_to_the_past_is_rejected(self):
        interview = self.make_interview()
        past = (timezone.now() - timedelta(days=1)).isoformat()
        self.client.force_authenticate(user=self.rec1)
        response = self.client.patch(
            f'/api/interviews/{interview.id}/', {'scheduled_at': past}, format='json'
        )
        self.assertEqual(response.status_code, 400)