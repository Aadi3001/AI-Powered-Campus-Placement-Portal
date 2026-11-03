from rest_framework.test import APITestCase

from accounts.models import User

from .models import Notification
from .utils import notify

PASSWORD = 'TestPass123'


class NotificationApiTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', password=PASSWORD, role='STUDENT')
        self.bob = User.objects.create_user('bob', password=PASSWORD, role='RECRUITER')
        notify(self.alice, 'First')
        notify(self.alice, 'Second')
        notify(self.bob, 'For Bob only')

    def test_user_sees_only_their_own_notifications_newest_first(self):
        self.client.force_authenticate(user=self.alice)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([n['message'] for n in response.data], ['Second', 'First'])

    def test_unread_count_and_mark_read(self):
        self.client.force_authenticate(user=self.alice)
        self.assertEqual(self.client.get('/api/notifications/unread-count/').data['count'], 2)
        first = Notification.objects.get(user=self.alice, message='First')
        response = self.client.post(f'/api/notifications/{first.id}/read/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/api/notifications/unread-count/').data['count'], 1)

    def test_cannot_mark_someone_elses_notification(self):
        self.client.force_authenticate(user=self.alice)
        bobs = Notification.objects.get(user=self.bob)
        response = self.client.post(f'/api/notifications/{bobs.id}/read/')
        self.assertEqual(response.status_code, 404)
        bobs.refresh_from_db()
        self.assertFalse(bobs.is_read)

    def test_read_all_only_affects_the_current_user(self):
        self.client.force_authenticate(user=self.alice)
        response = self.client.post('/api/notifications/read-all/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/api/notifications/unread-count/').data['count'], 0)
        self.assertFalse(Notification.objects.get(user=self.bob).is_read)

    def test_anonymous_is_refused(self):
        self.assertEqual(self.client.get('/api/notifications/').status_code, 401)