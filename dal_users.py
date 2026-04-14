import sqlite3
from passlib.context import CryptContext
import hashlib

"""
Module for handling user-related database operations.
"""

DB_NAME = "users.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_connection():
    """ Creates and returns a connection to the SQLite database. """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_table_users():
    """
    Initializes the users table in the database if it doesn't exist.
    """
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """
    with get_connection() as conn:
        conn.execute(query)

def hash_password(password: str):
    """ Hashes a plain-text password using SHA256 and bcrypt for security. """
    sha_password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha_password)

def insert_user(user_name, email, password):
    """ Inserts a new user into the database with an encrypted password. """
    query = "INSERT INTO users (user_name, email, password) VALUES (?, ?, ?)"
    try:
        with get_connection() as conn:
            conn.execute(query, (user_name, email, hash_password(password)))
        return True
    except sqlite3.IntegrityError:
        return None

def get_user_by_username(user_name):
    """ Fetches a single user record from the database based on the username. """
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_name = ?", (user_name,)).fetchone()
    return dict(row) if row else None

def get_all_users():
    """
    Fetches all registered users from the database for the management page.
    """
    with get_connection() as conn:
        rows = conn.execute("SELECT id, user_name, email FROM users").fetchall()
    return [dict(row) for row in rows]

def verify_password(plain_password: str, hashed_password: str):
    """ Compares a plain-text password with the stored hash to verify identity. """
    sha_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha_password, hashed_password)

def update_user_email(user_id, new_email):
    """
    Updates the email address of a specific user by their ID.
    """
    query = "UPDATE users SET email = ? WHERE id = ?"
    with get_connection() as conn:
        conn.execute(query, (new_email, user_id))

def delete_user(user_id):
    """
    Permanently removes a user from the database based on their ID.
    """
    query = "DELETE FROM users WHERE id = ?"
    with get_connection() as conn:
        conn.execute(query, (user_id,))