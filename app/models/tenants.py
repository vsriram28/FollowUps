from app import db


class Tenant(db.Model):
    __tablename__ = 'Tenants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Add other tenant attributes here as needed

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
            # Include other attributes as needed
        }
