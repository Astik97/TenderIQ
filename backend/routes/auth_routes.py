from flask import Blueprint, render_template,request
import bcrypt
from flask import session, redirect, flash
from backend.utils.db import get_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id,password
        FROM users
        WHERE email=%s
        """

        cursor.execute(query,(email,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            stored_hash = user[1]
            if bcrypt.checkpw(
                password.encode('utf-8'),
                stored_hash.encode('utf-8')):
                
                session['user_id'] = user[0]
                return redirect('/dashboard')
            
            flash("Invalid login credentials.", "error")
    return render_template('login.html')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()

        email = request.form["email"].strip()

        password = request.form["password"]

        conn = get_connection()

        cursor = conn.cursor()

        # ----------------------------
        # Check if email already exists
        # ----------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()

            conn.close()

            flash("Email already exists. Please use a different email.", "error")
            
            return redirect("/register")

        # ----------------------------
        # Hash Password
        # ----------------------------

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # ----------------------------
        # Insert User
        # ----------------------------

        cursor.execute(
            """
            INSERT INTO users 
            (
                username,
                email,
                password
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                username,
                email,
                hashed_password
            )
        )

        conn.commit()

        cursor.close()

        conn.close()

        flash("Registration successful! Please log in.", "success")

        return redirect("/login")

    return render_template("register.html")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')