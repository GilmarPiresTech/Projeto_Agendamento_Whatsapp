from flask import Blueprint, jsonify

# Criação do blueprint principal
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message": "Bem-vindo ao sistema de agendamento de WhatsApp!"})
