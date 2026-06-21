from flask import Flask, session, render_template, redirect, request
import sqlite3

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


### Register rout ###
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO user(username, email, password) VALUES(?, ?, ?)", (username, email, password))

        conn.commit()
        conn.close

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
        
        cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password)) #methana username and password check karanawa

        user = cursor.fetchone()

        conn.close()

        if user:
            # return render_template("dashboard.html")
            session["username"] = username #session aran username eka save karagannawa
            return redirect("/dashboard")
        else:
            return "Invalid username or Password"
        
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
