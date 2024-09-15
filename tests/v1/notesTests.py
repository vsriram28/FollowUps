import unittest
from app import app, db, Tenant, User, Meeting, Note
from datetime import datetime

class TestNotesAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

        # Sample Data for Tenants, Users, and Meetings (needed for foreign key relationships)
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

        # Sample Data for Notes
        self.note1 = Note(tenant_id=self.tenant.id, user_id=self.user.id, meeting_id=self.meeting.id,
                          content="This is the first test note. #followup_task1")
        self.note2 = Note(tenant_id=self.tenant.id, user_id=self.user.id, meeting_id=self.meeting.id,
                          content="This is the second test note with multiple lines.\nAnd a second line. #followup_task2")
        db.session.add_all([self.note1, self.note2])
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Create Note Tests

    def test_create_note_success(self):
        response = self.app.post('/notes', json={
            'tenant_id': self.tenant.id,
            'user_id': self.user.id,
            'meeting_id': self.meeting.id,
            'content': 'This is a new note. #followup_task3'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['tenant_id'], self.tenant.id)
        self.assertEqual(data['user_id'], self.user.id)
        self.assertEqual(data['meeting_id'], self.meeting.id)
        self.assertEqual(data['content'], 'This is a new note. #followup_task3')

        # Verify the note was added to the database
        note = Note.query.filter_by(content='This is a new note. #followup_task3').first()
        self.assertIsNotNone(note)

    def test_create_note_failure_missing_data(self):
        response = self.app.post('/notes', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    # Read Notes Tests

    def test_get_all_notes(self):
        response = self.app.get('/notes')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    # Read Note by ID Tests

    def test_get_note_by_id_success(self):
        response = self.app.get(f'/notes/{self.note1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.note1.id)
        self.assertEqual(data['content'], self.note1.content)

    def test_get_note_by_id_failure_not_found(self):
        response = self.app.get('/notes/999')
        self.assertEqual(response.status_code, 404)

    # Update Note Tests

    def test_update_note_success(self):
        response = self.app.put(f'/notes/{self.note1.id}', json={'content': 'Updated note content. #updated_task'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.note1.id)
        self.assertEqual(data['content'], 'Updated note content. #updated_task')

        # Verify the update in the database
        note = Note.query.get(self.note1.id)
        self.assertEqual(note.content, 'Updated note content. #updated_task')

    def test_update_note_failure_not_found(self):
        response = self.app.put('/notes/999', json={'content': 'Updated content'})
        self.assertEqual(response.status_code, 404)

    # Delete Note Tests

    def test_delete_note_success(self):
        response = self.app.delete(f'/notes/{self.note1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Note deleted successfully')

        # Verify deletion from the database
        note = Note.query.get(self.note1.id)
        self.assertIsNone(note)

    def test_delete_note_failure_not_found(self):
        response = self.app.delete('/notes/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()