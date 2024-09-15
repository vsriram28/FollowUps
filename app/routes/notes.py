from flask import render_template
from flask import Flask, request, jsonify
from app import app, db
from app.models.notes import Note

# Create (POST)
@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    new_note = Note(
        tenant_id=data['tenant_id'],
        user_id=data['user_id'],
        content=data['content'],
        meeting_id=data['meeting_id']
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify(new_note.to_dict()), 201

# Read (GET)
@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.to_dict() for note in notes])

# Read by ID (GET)
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

# Update (PUT)
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    note.content = data['content']
    db.session.commit()
    return jsonify(note.to_dict())

# Delete (DELETE)
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'}), 200
