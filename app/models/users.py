from app import db

class User(db.Model):
    __tablename__ = 'Users'  # Explicitly set table name if needed
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('Tenants.id'), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)  # Assuming this is needed

    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'username': self.username,
            'user_id': self.user_id
            # Exclude 'password' for security
        }
    