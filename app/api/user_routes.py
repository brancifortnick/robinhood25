from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy.orm import query
from app.models import User, db

user_routes = Blueprint('users', __name__)


@user_routes.route('/balance/<amount>/<operator>', methods=['POST', 'PUT', 'OPTIONS'])
@login_required
def user_balance(amount, operator):
    print(f"=== USER BALANCE REQUEST ===")
    print(f"Amount: {amount}, Operator: {operator}")
    print(f"Request method: {request.method}")
    
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return {'error': 'Invalid amount'}, 400
    
    user = User.query.filter(
        User.id == current_user.id).one_or_none()
    
    if not user:
        return {'error': 'User not found'}, 404
    
    if operator == 'add':
        user.cash_balance += amount
        print(f"Adding ${amount}, new balance: ${user.cash_balance}")
    elif operator == 'subtract':
        user.cash_balance -= amount
        print(f"Subtracting ${amount}, new balance: ${user.cash_balance}")
    else:
        return {'error': 'Invalid operator'}, 400
    
    db.session.add(user)
    db.session.commit()
    print("Balance updated successfully")
    return jsonify(user.to_dict())


@user_routes.route('/')
@login_required
def users():
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def user(id):
    user = User.query.get(id)
    return user.to_dict()
