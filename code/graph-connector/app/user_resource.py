from flask import (
    Blueprint, g, request, session
)

from werkzeug.security import generate_password_hash, gen_salt

from .db import get_db

from .auth import admin_login_required
from .request_utils import get_numeric_query_parameter

SALT_LENGTH = 16

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.get('')
@admin_login_required
def get_users():
    limit = get_numeric_query_parameter('limit', 10)
    page = max(get_numeric_query_parameter('page', 1) - 1, 0)

    db = get_db()

    user_name_search_input = request.args.get('keys')

    try:
        if user_name_search_input:
            found_users = db.execute(
                f"""
                SELECT username FROM user
                WHERE deleted = 0
                AND username REGEXP '.*{user_name_search_input}.*'
                LIMIT {limit}
                OFFSET {page * limit}
                """
            ).fetchall()
        else:
            found_users = db.execute(
                f"""
                SELECT username FROM user
                WHERE deleted = 0
                LIMIT {limit}
                OFFSET {page * limit}
                """
            ).fetchall()
    except db.Error as e:
        print(e)
        return {}, 500

    users = []
    for row in found_users:
        users.append({
            'username': row['username']
        })

    return users, 200


@bp.post('/<string:username>')
@admin_login_required
def register_user(username: str):
    registration_data = request.get_json()

    password = registration_data["password"]
    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error is None:
        try:
            salt = gen_salt(SALT_LENGTH)
            db.execute(
                "INSERT INTO user (username, salt, password, deleted) VALUES (?, ?, ?, ?)",
                (username, salt, generate_password_hash(password + salt), 0),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
        else:
            return f"Successfully created user {username}", 200

    return error, 409


@bp.delete('/<string:username>')
@admin_login_required
def delete_user(username: str):
    # Do not delete user from database, instead set deleted flag
    db = get_db()

    try:
        db.execute(
            f"""
            UPDATE user SET deleted = 1 WHERE username = '{username}'
            """
        )
        db.commit()
    except db.Error:
        return 'Could not delete specified user.', 404

    return f'Deleted user {username}', 200
