from flask import jsonify, make_response, request, Blueprint
from data.users import User
from data import db_session


blueprint = Blueprint(
    'api_user',
    __name__,
    template_folder='templates')


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict()
                 for item in users],
            'status': 200
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if user:
        return jsonify(
            {
                'user': user.to_dict(),
                'status': 200
            }
        )
    return jsonify(
        {
            'error': f'no user with id={user_id}',
            'status': 404
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return jsonify({'error': 'Empty request', 'status': 400})
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "position", "speciality", "address", "email", "hashed_password"]):
        return jsonify({'error': 'Bad request',
                       'status': 400})
    db_sess = db_session.create_session()
    user = User()
    user.surname = request.json["surname"]
    user.name = request.json["name"]
    user.age = request.json["age"]
    user.position = request.json["position"]
    user.speciality = request.json["speciality"]
    user.address = request.json["address"]
    user.email = request.json["email"]
    user.hashed_password = request.json["password"]
    user.set_password(user.hashed_password)
    db_sess.add(user)
    db_sess.commit()
    return jsonify({"id": user.id, 'status': 200})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request', 'status': 400})
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "position", "speciality", "address"]):
        return jsonify({'error': 'Bad request', 'status': 400})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    user.address = request.json["address"]
    user.name = request.json["name"]
    user.speciality = request.json["speciality"]
    user.age = request.json["age"]
    user.position = request.json['position']
    user.surname = request.json["surname"]
    db_sess.add(user)
    db_sess.commit()
    return jsonify(
        {
            'edited_user': user.to_dict(), 'status': 200
        }
    )


@blueprint.route('/api/user_delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found', 'status': 404})
    if user_id == 1:
        return jsonify({"error": "Can`t delete captain", 'status': 418})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK', 'status': 200})
