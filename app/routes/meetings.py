from datetime import datetime

from flask import render_template
from flask import Flask, request, jsonify
from app import app, db
from app.models.meetings import Meeting
from app.models.notes import Note


# Create (POST)
@app.route('/meetings', methods=['POST'])
def create_meeting():
    data = request.get_json()
    new_meeting = Meeting(
        tenant_id=data['tenant_id'],
        user_id=data['user_id'],
        title=data['title'],
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time'])
    )
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify(new_meeting.to_dict()), 201

# Read (GET)
@app.route('/meetings', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    return jsonify([meeting.to_dict() for meeting in meetings])

# Read by ID (GET)
@app.route('/meetings/<int:meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    return jsonify(meeting.to_dict())

# Update (PUT)
@app.route('/meetings/<int:meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    data = request.get_json()

    if 'title' in data:
        meeting.title = data['title']
    if 'start_time' in data:
        meeting.start_time = datetime.fromisoformat(data['start_time'])
    if 'end_time' in data:
        meeting.end_time = datetime.fromisoformat(data['end_time'])
    # Update other meeting attributes as needed

    db.session.commit()
    return jsonify(meeting.to_dict())

# Delete (DELETE)
@app.route('/meetings/<int:meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    db.session.delete(meeting)
    db.session.commit()
    return jsonify({'message': 'Meeting deleted successfully'}), 200

# Get all the meetings for a given date
@app.route('/meetings_by_date/<date_str>')
def meetings_by_date(date_str):
    selected_date = datetime.strptime(date_str, '%m%d%Y').date()
    print(selected_date)
    meetings = Meeting.query.filter(db.cast(Meeting.start_time, db.Date) == selected_date).all()
    # print(meetings)
    return jsonify([meeting.to_dict() for meeting in meetings])

# Meetings with the associated Notes for a given day
@app.route('/meetings_by_date_with_notes/<date_str>')
def meetings_by_date_with_notes(date_str):
    # print ("Given date: " + date_str)
    selected_date = datetime.strptime(date_str, '%m%d%Y').date()
    meetings = Meeting.query.filter(db.cast(Meeting.start_time, db.Date) == selected_date).all()

    # Fetch associated notes for each meeting
    meetings_with_notes = []
    for meeting in meetings:
        notes = Note.query.filter_by(meeting_id=meeting.id).all()
        meetings_with_notes.append({
            'meeting': meeting.to_dict(),
            'notes': [note.to_dict() for note in notes]
        })
    # print(meetings_with_notes)
    return jsonify(meetings_with_notes)