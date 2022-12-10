import functools
import os

from flask import (
    Blueprint, g, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash, gen_salt

# from flaskr.db import get_db
from .db import get_db

SALT_LENGTH = 16

SECRET_TOKEN = os.getenv('SECRET_TOKEN')
if not SECRET_TOKEN:
    SECRET_TOKEN = 'debug'
    print('No secret defined! Please provide secret to ensure safe operations! Not for production use!')

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return "Forbidden. Login required.", 403

        return view(**kwargs)

    return wrapped_view


def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return "Forbidden. Admin privileges required.", 403

        return view(**kwargs)

    return wrapped_view


@bp.post('/user/register')
@admin_login_required
def register():
    registration_data = request.get_json()

    username = registration_data["username"]
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
                "INSERT INTO user (username, salt, password) VALUES (?, ?, ?)",
                (username, salt, generate_password_hash(password + salt)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
        else:
            return f"Successfully created user {username}", 200

    return error, 409


@bp.post('/admin/register')
def admin_register():
    registration_data = request.get_json()

    secret_token = registration_data['secret']
    db = get_db()
    error = None

    if secret_token != SECRET_TOKEN:
        error = "Incorrect secret token."

    username = registration_data["username"]
    password = registration_data["password"]

    if not password:
        error = 'Password is required.'
    elif len(password) < 15:
        error = 'Password should be at least 15 characters long.'
    elif not username:
        error = 'Username is required.'

    if error is None:
        try:
            salt = gen_salt(SALT_LENGTH)
            db.execute(
                "INSERT INTO admin (username, salt, password) VALUES (?, ?, ?)",
                (username, salt, generate_password_hash(password + salt)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"Admin {username} is already registered."
        else:
            return f"Successfully created admin {username}", 200

    return error, 409


@bp.post('/user/login')
def login():
    login_data = request.get_json()

    username = login_data["username"]
    password = login_data["password"]
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password + user['salt']):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return "Logged in", 200

    return error, 403


@bp.post('/admin/login')
def admin_login():
    login_data = request.get_json()

    username = login_data['username']
    password = login_data['password']
    db = get_db()
    error = None
    admin = db.execute(
        'SELECT * FROM admin WHERE username = ?', (username,)
    ).fetchone()

    if admin is None:
        error = 'Incorrect username.'
    elif not check_password_hash(admin['password'], password + admin['salt']):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['admin_id'] = admin['id']
        return "Logged in", 200

    return error, 403


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    admin_id = session.get('admin_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

    if admin_id is None:
        g.admin = None
    else:
        g.admin = get_db().execute(
            'SELECT * FROM admin WHERE id = ?', (admin_id,)
        ).fetchone()


@bp.post('/logout')
def logout():
    session.clear()
    return "Logged out", 200
