from flask import render_template
from flask import Flask, request, jsonify
from app import app, db
from app.models.followups import FollowUpAction

# Create (POST)
@app.route('/followup_actions', methods=['POST'])
def create_follow_up_action():
    data = request.get_json()
    new_action = FollowUpAction(
        tenant_id=data['tenant_id'],
        user_id=data['user_id'],
        meeting_id=data['meeting_id'],
        note_id=data['note_id'],
        hashtag=data['hashtag'],
        full_action=data['full_action'],
        status=data['status']
    )
    db.session.add(new_action)
    db.session.commit()
    return jsonify(new_action.to_dict()), 201


# Read (GET)
@app.route('/followup_actions', methods=['GET'])
def get_follow_up_actions():
    actions = FollowUpAction.query.all()
    return jsonify([action.to_dict() for action in actions])


# Read by ID (GET)
@app.route('/followup_actions/<int:action_id>', methods=['GET'])
def get_follow_up_action(action_id):
    action = FollowUpAction.query.get_or_404(action_id)
    return jsonify(action.to_dict())


# Update (PUT)
@app.route('/followup_actions/<int:action_id>', methods=['PUT'])
def update_follow_up_action(action_id):
    action = FollowUpAction.query.get_or_404(action_id)
    data = request.get_json()

    # Update fields if provided
    if 'status' in data:
        action.status = data['status']
    # ... (Update other fields as needed, e.g., full_action if allowed)

    db.session.commit()
    return jsonify(action.to_dict())


# Delete (DELETE)
@app.route('/followup_actions/<int:action_id>', methods=['DELETE'])
def delete_follow_up_action(action_id):
    action = FollowUpAction.query.get_or_404(action_id)
    db.session.delete(action)
    db.session.commit()
    return jsonify({'message': 'Follow-up action deleted successfully'}), 200

# Follow-up items list based on their status
@app.route('/followup_actions_for_given_status/<status>')
def get_follow_up_actions_for_given_status(status):
    actions = FollowUpAction.query.filter_by(status=status).order_by(FollowUpAction.created_at).all()
    return jsonify([action.to_dict() for action in actions])

