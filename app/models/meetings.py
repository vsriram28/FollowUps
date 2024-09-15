from app import db

class Meeting(db.Model):
    __tablename__ = 'Meetings'  # Explicitly set table name if needed
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('Tenants.id'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('Users.user_id'), nullable=False)  # Using user_id as FK
    title = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'title': self.title,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat()
        }
