from flask import render_template
from flask import Flask, request, jsonify
from app import app, db
from app.models.users import User

# Create (POST)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        tenant_id=data['tenant_id'],
        username=data['username'],
        password=data['password'],  # Handle password securely in a real app
        user_id=data['user_id']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


# Read (GET)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# Read by ID (GET)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


# Update (PUT)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    # Update fields, handle password securely if needed
    if 'username' in data:
        user.username = data['username']
    # ... (similarly for other updatable fields)

    db.session.commit()
    return jsonify(user.to_dict())


# Delete (DELETE)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
