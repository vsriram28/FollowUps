import unittest
from app import app, db, Tenant, User  # Import necessary modules

class TestUsersAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

        # Sample Data for Tenants (needed for foreign key relationship)
        self.tenant = Tenant(name="Test Tenant")
        db.session.add(self.tenant)
        db.session.commit()

        # Sample Data for Users
        self.user1 = User(tenant_id=self.tenant.id, username="user1", password="password123", user_id=101)
        self.user2 = User(tenant_id=self.tenant.id, username="user2", password="password456", user_id=102)
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Create User Tests

    def test_create_user_success(self):
        response = self.app.post('/users', json={
            'tenant_id': self.tenant.id,
            'username': 'new_user',
            'password': 'new_password',
            'user_id': 103
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['tenant_id'], self.tenant.id)
        self.assertEqual(data['username'], 'new_user')
        self.assertEqual(data['user_id'], 103)

        # Verify the user was added to the database
        user = User.query.filter_by(username='new_user').first()
        self.assertIsNotNone(user)

    def test_create_user_failure_duplicate_username(self):
        response = self.app.post('/users', json={
            'tenant_id': self.tenant.id,
            'username': 'user1',  # Duplicate username
            'password': 'some_password',
            'user_id': 104
        })
        self.assertEqual(response.status_code, 400)  # Or another appropriate error code
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_user_failure_missing_data(self):
        response = self.app.post('/users', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    # Read Users Tests

    def test_get_all_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)  # We added 2 users in setUp

    # Read User by ID Tests

    def test_get_user_by_id_success(self):
        response = self.app.get(f'/users/{self.user1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.user1.id)
        self.assertEqual(data['tenant_id'], self.tenant.id)
        self.assertEqual(data['username'], self.user1.username)
        self.assertEqual(data['user_id'], self.user1.user_id)

    def test_get_user_by_id_failure_not_found(self):
        response = self.app.get('/users/999')  # Non-existent ID
        self.assertEqual(response.status_code, 404)

    # Update User Tests

    def test_update_user_success(self):
        response = self.app.put(f'/users/{self.user1.id}', json={'username': 'updated_username'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.user1.id)
        self.assertEqual(data['username'], 'updated_username')

        # Verify the update in the database
        user = User.query.get(self.user1.id)
        self.assertEqual(user.username, 'updated_username')

    def test_update_user_failure_not_found(self):
        response = self.app.put('/users/999', json={'username': 'updated_name'})
        self.assertEqual(response.status_code, 404)

    # Delete User Tests

    def test_delete_user_success(self):
        response = self.app.delete(f'/users/{self.user1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'User deleted successfully')

        # Verify deletion from the database
        user = User.query.get(self.user1.id)
        self.assertIsNone(user)

    def test_delete_user_failure_not_found(self):
        response = self.app.delete('/users/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()