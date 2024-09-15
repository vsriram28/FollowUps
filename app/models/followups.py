from app import db
from datetime import datetime

class FollowUpAction(db.Model):
    __tablename__ = 'FollowUpActions'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('Tenants.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('Meetings.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('Notes.id'), nullable=False)
    hashtag = db.Column(db.String(255), nullable=False)
    full_action = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'meeting_id': self.meeting_id,
            'note_id': self.note_id,
            'hashtag': self.hashtag,
            'full_action': self.full_action,
            'status': self.status
        }

