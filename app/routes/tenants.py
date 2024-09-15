from flask import render_template
from flask import Flask, request, jsonify
from app import app, db
from app.models.tenants import Tenant


# Create (POST)
@app.route('/tenants', methods=['POST'])
def create_tenant():
    data = request.get_json()
    new_tenant = Tenant(name=data['name'])  # Add other attributes as needed
    db.session.add(new_tenant)
    db.session.commit()
    return jsonify(new_tenant.to_dict()), 201


# Read (GET)
@app.route('/tenants', methods=['GET'])
def get_tenants():
    tenants = Tenant.query.all()
    return jsonify([tenant.to_dict() for tenant in tenants])


# Read by ID (GET)
@app.route('/tenants/<int:tenant_id>', methods=['GET'])
def get_tenant(tenant_id):
    tenant = Tenant.query.get_or_404(tenant_id)
    return jsonify(tenant.to_dict())


# Update (PUT)
@app.route('/tenants/<int:tenant_id>', methods=['PUT'])
def update_tenant(tenant_id):
    tenant = Tenant.query.get_or_404(tenant_id)
    data = request.get_json()
    tenant.name = data['name']  # Update other attributes as needed
    db.session.commit()
    return jsonify(tenant.to_dict())


# Delete (DELETE)
@app.route('/tenants/<int:tenant_id>', methods=['DELETE'])
def delete_tenant(tenant_id):
    tenant = Tenant.query.get_or_404(tenant_id)
    db.session.delete(tenant)
    db.session.commit()
    return jsonify({'message': 'Tenant deleted successfully'}), 200
