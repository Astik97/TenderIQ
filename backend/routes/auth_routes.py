from flask import (
    Blueprint, 
    render_template,
    request,
    session, 
    redirect, 
    flash
)
import bcrypt
from backend.utils.db import get_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email'].strip().lower()
        
        password = request.form['password']
        
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id,username,password
        FROM users
        WHERE email=%s
        """

        cursor.execute(query,(email,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            stored_hash = user[2]

            if bcrypt.checkpw (
                password.encode('utf-8'),
                stored_hash.encode('utf-8')):
                
                session['user_id'] = user[0]

                session["username"] = user[1]

                flash(f"Welcome back, {user[1]}!","success")

                return redirect('/dashboard')
            
            flash("Unable to login. Please try again.", "error")

    return render_template('login.html')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()

        email = request.form["email"].strip().lower()

        password = request.form["password"]

        conn = get_connection()

        cursor = conn.cursor()

        # ----------------------------
        # Validate Password Length
        # ----------------------------
        
        if len(password) < 8:
            
            flash("Password must be at least 8 characters long.","error")

            return redirect("/register")


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

    flash("Logged out successfully.","success")

    return redirect('/login')