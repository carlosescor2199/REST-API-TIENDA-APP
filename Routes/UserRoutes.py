from API import app
from flask import request, jsonify
import bcrypt

from DATABASE import db
from Models.User import User, user_schema


@app.route('/signup', methods=["POST"])
def signup():
    firstname = request.json.get('firstname', None)
    lastname = request.json.get('lastname', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    confirm_password = request.json.get('confirm_password', None)

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            "error": "El email ya está en uso"
        }), 400
    if not firstname:
        return jsonify({
            "error": "El nombre no puede estar vacio"
        }), 400
    if not lastname:
        return jsonify({
            "error": "El apellido no puede estar vacio"
        }), 400
    if not email:
        return jsonify({
            "error": "El email no puede estar vacio"
        }), 400
    if not password:
        return jsonify({
            "error": "La contraseña no puede estar vacía"
        }), 400
    if not confirm_password:
        return jsonify({
            "error": "Confirmar contraseña no puede estar vacio"
        }), 400
    if password != confirm_password:
        return jsonify({
            "error": "Las contraseñas no coinciden"
        }), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(firstname, lastname, email, hashed)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/login', methods=["POST"])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return jsonify({
            "error": "El email no puede estar vacio"
        }), 400
    if not password:
        return jsonify({
            "error": "La contraseña no puede estar vacía"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error": "Usuario no encontrado"
        }), 400

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({
            "error": "Contraseña incorrecta"
        })

    return user_schema.jsonify(user)
