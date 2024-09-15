import unittest
from app import app, db, Tenant  # Import your Flask app, database, and Tenant model

class TestTenantsAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

        # Sample Data for Tenants
        self.tenant1 = Tenant(name="Test Tenant 1")
        self.tenant2 = Tenant(name="Test Tenant 2")
        db.session.add_all([self.tenant1, self.tenant2])
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Create Tenant Tests

    def test_create_tenant_success(self):
        response = self.app.post('/tenants', json={'name': 'New Tenant'})
        self.assertEqual(response.status_code, 201)  # Expect 201 Created
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'New Tenant')

        # Verify the tenant was added to the database
        tenant = Tenant.query.filter_by(name='New Tenant').first()
        self.assertIsNotNone(tenant)

    def test_create_tenant_failure_duplicate_name(self):
        response = self.app.post('/tenants', json={'name': 'Test Tenant 1'})
        self.assertEqual(response.status_code, 400)  # Or another appropriate error code
        data = response.get_json()
        self.assertIn('error', data)  # Expect an error message

    def test_create_tenant_failure_missing_name(self):
        response = self.app.post('/tenants', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    # Read Tenants Tests

    def test_get_all_tenants(self):
        response = self.app.get('/tenants')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)  # We added 2 tenants in setUp

    # Read Tenant by ID Tests

    def test_get_tenant_by_id_success(self):
        response = self.app.get(f'/tenants/{self.tenant1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.tenant1.id)
        self.assertEqual(data['name'], self.tenant1.name)

    def test_get_tenant_by_id_failure_not_found(self):
        response = self.app.get('/tenants/999')  # Non-existent ID
        self.assertEqual(response.status_code, 404)

    # Update Tenant Tests

    def test_update_tenant_success(self):
        response = self.app.put(f'/tenants/{self.tenant1.id}', json={'name': 'Updated Tenant Name'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], self.tenant1.id)
        self.assertEqual(data['name'], 'Updated Tenant Name')

        # Verify the update in the database
        tenant = Tenant.query.get(self.tenant1.id)
        self.assertEqual(tenant.name, 'Updated Tenant Name')

    def test_update_tenant_failure_not_found(self):
        response = self.app.put('/tenants/999', json={'name': 'Updated Name'})
        self.assertEqual(response.status_code, 404)

    # Delete Tenant Tests

    def test_delete_tenant_success(self):
        response = self.app.delete(f'/tenants/{self.tenant1.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Tenant deleted successfully')

        # Verify deletion from the database
        tenant = Tenant.query.get(self.tenant1.id)
        self.assertIsNone(tenant)

    def test_delete_tenant_failure_not_found(self):
        response = self.app.delete('/tenants/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()