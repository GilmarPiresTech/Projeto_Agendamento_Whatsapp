from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.appointment import Appointment

appointments = Blueprint("appointments", __name__)

@appointments.route("/appointments", methods=["GET"])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([
        {
            "id": appointment.id,
            "user_id": appointment.user_id,
            "date": appointment.date.isoformat(),
            "type": appointment.type,
            "duration": appointment.duration,
        }
        for appointment in appointments
    ])

@appointments.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.json
    if not data.get("user_id") or not data.get("date") or not data.get("type") or not data.get("duration"):
        return jsonify({"error": "All fields are required"}), 400
    
    try:
        new_appointment = Appointment(
            user_id=data["user_id"],
            date=data["date"],
            type=data["type"],
            duration=data["duration"],
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"message": "Appointment created", "id": new_appointment.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
