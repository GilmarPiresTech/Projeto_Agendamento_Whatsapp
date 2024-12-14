from flask import Blueprint, request, jsonify
from sqlalchemy.exc import OperationalError
from app.extensions import db
from app.models.user import User

# Criação do blueprint para rotas principais
main = Blueprint("main", __name__)

# Rota para listar todos os usuários
@main.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return jsonify([
            {"id": user.id, "name": user.name, "phone": user.phone} for user in users
        ])
    except OperationalError as e:
        return jsonify({"error": "Database connection issue", "details": str(e)}), 500

# Rota para criar um novo usuário
@main.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.json
        if not data.get("name") or not data.get("phone"):
            return jsonify({"error": "Name and phone are required"}), 400

        new_user = User(name=data["name"], phone=data["phone"])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created", "id": new_user.id}), 201
    except OperationalError as e:
        db.session.rollback()
        return jsonify({"error": "Database connection issue", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
