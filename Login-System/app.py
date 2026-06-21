from flask import Flask, render_template, redirect, request, session, flash
import sqlite3

# password hashing module
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.secret_key = "mysecretkey" #session ekka use karanawa

### Database Create ###
def table_create():

    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                                                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                                        username TEXT, 
                                                        email TEXT, 
                                                        password TEXT )""")
    
    conn.commit()
    conn.close()

table_create()


### Register route ###
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        # password = request.form["password"]
        hashed_password = generate_password_hash("password")

        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        
        # username chekinkg(duplicate value chaking)
        cursor.execute("SELECT * FROM user WHERE username=?", (username,))

        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists!")
            conn.close()
            return redirect("/register")
        
        # email chekinkg(duplicate value chaking)
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))

        existing_email = cursor.fetchone()

        if existing_email:
            flash("Email already exists!")
            conn.close()
            return redirect("/register")

        # insert data in the table
        cursor.execute("INSERT INTO user(username, email, password) VALUES(?, ?, ?)", (username, email, hashed_password))

        conn.commit()
        conn.close()

        flash("Registration Successful! Please Login") #flash message
        return redirect("/login") #login page ekata redirect karanawa
    
    return render_template("register.html") #register page ekata redirect karanawa



### Login Route ###
@app.route("/login", methods=["GET", "POST"])
def login():

    # login validation
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # database check
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user WHERE username=?", (username,)) #methana username and password check karanawa

        user = cursor.fetchone()
        
        if user and check_password_hash(user[3], password):

            session["username"] = username

            return redirect("/dashboard")

        conn.close()

        if user:
            # return render_template("dashboard.html")
            session["username"] = username #session aran username eka save karagannawa
            return redirect("/dashboard")
        else:
            flash("Invalid username or password") #flash message
            return redirect("/login")
            
    return render_template("login.html")
        


### Dashboard route ###
@app.route("/dashboard")
def dashboard():

    if "username" not in session:#methana username eka session ekka save una username ekata samanada kiyala balanawa
        return redirect("/login")
    return render_template("dashboard.html", username=session["username"])




### logout route ###
@app.route("/logout")
def logout():
    session.pop("username", None)#save una username remove karanawa

    return redirect("/login")

app.run(debug=True)
