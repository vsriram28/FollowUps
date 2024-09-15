import unittest
from app import app, db, Tenant, User, Meeting, Note, FollowUpAction

class TestFollowUpActionsAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

        # Sample Data for Tenants, Users, Meetings, and Notes
        self.tenant = Tenant(name="Test Tenant")
        db.session.add(self.tenant)
        db.session.commit()

        self.user = User(tenant_id=self.tenant.id, username="testuser", password="password123", user_id=101)
        db.session.add(self.user)
        db.session.commit()

        self.meeting = Meeting(tenant_id=self.tenant.id, user_id=self.user.user_id, title="Test Meeting",
                               start_time=datetime(2023, 9, 1, 10, 0), end_time=datetime(2023, 9, 1, 12, 0))
        db.session.add(self.meeting)
        db.session.commit()

        self.note = Note(tenant_id=self.tenant.id, user_id=self.user.id, meeting_id=self.meeting.id,
                         content="This is a test note. #followup_task")
        db.session.add(self.note)
        db.session.commit()

        # Sample Data for FollowUpActions
        self.action1 = FollowUpAction(tenant_id=self.tenant.id, user_id=self.user.id, meeting_id=self.meeting.id,
                                      note_id=self.note.id, hashtag="#followup_task",
                                      full_action="This is a test note. #followup_task", status="pending")
        self.action2 = FollowUpAction(tenant_id=self.tenant.id, user_id=self.user.id, meeting_id=self.meeting.id,
                                      note_id=self.note.id, hashtag="#another_task",
                                      full_action="Another task in the same note. #another_task", status="in-progress")
        db.session.add_all([self.action1, self.action2])
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Create FollowUpAction Tests

    def test_create_follow_up_action_success(self):
        response = self.app.post('/followup_actions', json={
            'tenant_id': self.tenant.id,
            'user_id': self.user.id,
            'meeting_id': self.meeting.id,
            'note_id': self.note.id,
            'hashtag': '#new_task',
            'full_action': 'This is a new task. #new_task',
            'status': 'pending'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['hashtag'], '#new_task')
        self.assertEqual(data['status'], 'pending')

        # Verify the action was added to the database
        action = FollowUpAction.query.filter_by(hashtag='#new_task').first()
        self.assertIsNotNone(action)

    def test_create_follow_up_action_failure_missing_data(self):
        response = self.app.post('/followup_actions', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    # Read FollowUpActions Tests

    def test_get_all_follow_up_actions(self):
        response = self.app.get('/followup_actions')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    # Read FollowUpAction by ID Tests

    def test_get_follow_up_action_by_id_success(self):
        response = self.app.get(f'/followup_actions/{self.action1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.action1.id)
        self.assertEqual(data['hashtag'], self.action1.hashtag)
        self.assertEqual(data['status'], self.action1.status)

    def test_get_follow_up_action_by_id_failure_not_found(self):
        response = self.app.get('/followup_actions/999')
        self.assertEqual(response.status_code, 404)

    # Update FollowUpAction Tests

    def test_update_follow_up_action_success(self):
        response = self.app.put(f'/followup_actions/{self.action1.id}', json={'status': 'completed'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.action1.id)
        self.assertEqual(data['status'], 'completed')

        # Verify the update in the database
        action = FollowUpAction.query.get(self.action1.id)
        self.assertEqual(action.status, 'completed')

    def test_update_follow_up_action_failure_not_found(self):
        response = self.app.put('/followup_actions/999', json={'status': 'completed'})
        self.assertEqual(response.status_code, 404)

    # Delete FollowUpAction Tests

    def test_delete_follow_up_action_success(self):
        response = self.app.delete(f'/followup_actions/{self.action1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Follow-up action deleted successfully')

        # Verify deletion from the database
        action = FollowUpAction.query.get(self.action1.id)
        self.assertIsNone(action)

    def test_delete_follow_up_action_failure_not_found(self):
        response = self.app.delete('/followup_actions/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()