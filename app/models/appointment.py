from app.extensions import db

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Em minutos
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship("User", backref="appointments")

    def __repr__(self):
        return f"<Appointment {self.type} on {self.date}>"
