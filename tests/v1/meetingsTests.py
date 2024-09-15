import unittest
from app import app, db, Tenant, User, Meeting
from datetime import datetime

class TestMeetingsAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

        # Sample Data for Tenants and Users (needed for foreign key relationships)
        self.tenant = Tenant(name="Test Tenant")
        db.session.add(self.tenant)
        db.session.commit()

        self.user = User(tenant_id=self.tenant.id, username="testuser", password="password123", user_id=101)
        db.session.add(self.user)
        db.session.commit()

        # Sample Data for Meetings
        self.meeting1 = Meeting(tenant_id=self.tenant.id, user_id=self.user.user_id, title="Meeting 1",
                                start_time=datetime(2023, 9, 1, 10, 0), end_time=datetime(2023, 9, 1, 12, 0))
        self.meeting2 = Meeting(tenant_id=self.tenant.id, user_id=self.user.user_id, title="Meeting 2",
                                start_time=datetime(2023, 9, 2, 14, 30), end_time=datetime(2023, 9, 2, 16, 0))
        db.session.add_all([self.meeting1, self.meeting2])
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Create Meeting Tests

    def test_create_meeting_success(self):
        response = self.app.post('/meetings', json={
            'tenant_id': self.tenant.id,
            'user_id': self.user.user_id,
            'title': 'New Meeting',
            'start_time': '2023-09-03T09:00:00',
            'end_time': '2023-09-03T11:00:00'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['tenant_id'], self.tenant.id)
        self.assertEqual(data['user_id'], self.user.user_id)
        self.assertEqual(data['title'], 'New Meeting')

        # Verify the meeting was added to the database
        meeting = Meeting.query.filter_by(title='New Meeting').first()
        self.assertIsNotNone(meeting)

    def test_create_meeting_failure_missing_data(self):
        response = self.app.post('/meetings', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    # Read Meetings Tests

    def test_get_all_meetings(self):
        response = self.app.get('/meetings')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    # Read Meeting by ID Tests

    def test_get_meeting_by_id_success(self):
        response = self.app.get(f'/meetings/{self.meeting1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.meeting1.id)
        self.assertEqual(data['tenant_id'], self.tenant.id)
        self.assertEqual(data['user_id'], self.user.user_id)
        self.assertEqual(data['title'], self.meeting1.title)

    def test_get_meeting_by_id_failure_not_found(self):
        response = self.app.get('/meetings/999')
        self.assertEqual(response.status_code, 404)

    # Update Meeting Tests

    def test_update_meeting_success(self):
        response = self.app.put(f'/meetings/{self.meeting1.id}', json={'title': 'Updated Meeting Title'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.meeting1.id)
        self.assertEqual(data['title'], 'Updated Meeting Title')

        # Verify the update in the database
        meeting = Meeting.query.get(self.meeting1.id)
        self.assertEqual(meeting.title, 'Updated Meeting Title')

    def test_update_meeting_failure_not_found(self):
        response = self.app.put('/meetings/999', json={'title': 'Updated Title'})
        self.assertEqual(response.status_code, 404)

    # Delete Meeting Tests

    def test_delete_meeting_success(self):
        response = self.app.delete(f'/meetings/{self.meeting1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Meeting deleted successfully')

        # Verify deletion from the database
        meeting = Meeting.query.get(self.meeting1.id)
        self.assertIsNone(meeting)

    def test_delete_meeting_failure_not_found(self):
        response = self.app.delete('/meetings/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()