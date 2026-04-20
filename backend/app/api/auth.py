from flask import Blueprint, request, jsonify
from app.core.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing email or password"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "User already exists"}), 400
        
    new_user = User(email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad email or password"}), 401
    return jsonify({
        "access_token": create_access_token(identity=user.id),
        "user": {"id": user.id, "email": user.email, "role": user.role}
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = User.query.get(get_jwt_identity())
    return jsonify({"id": user.id, "email": user.email, "role": user.role}), 200
