from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------------- DATABASE CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    student_class = db.Column(db.String(50))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    age = db.Column(db.Integer)
    experience = db.Column(db.Integer)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))

# ---------------- HOME ----------------
@app.route("/")
def index():
    students = Student.query.all()
    teachers = Teacher.query.all()
    return render_template("index.html",
                           students=students,
                           teachers=teachers)

# =============about==================
@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    user = User(
        fname=request.form.get("fname"),
        lname=request.form.get("lname"),
        email=request.form.get("email"),
        password=request.form.get("password"),
        role=request.form.get("role")
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("home"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email,
                                password=password).first()

    if user:
        return "Login Successful ✅"
    return "Invalid Login ❌"

# ---------------- ADD STUDENT ----------------
@app.route("/add_student", methods=["POST"])
def add_student():
    s = Student(
        name=request.form.get("name"),
        email=request.form.get("email"),
        age=request.form.get("age"),
        student_class=request.form.get("class")
    )
    db.session.add(s)
    db.session.commit()
    return redirect(url_for("home"))

# ---------------- ADD TEACHER ----------------
@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    t = Teacher(
        name=request.form.get("name"),
        subject=request.form.get("subject"),
        age=request.form.get("age"),
        experience=request.form.get("experience")
    )
    db.session.add(t)
    db.session.commit()
    return redirect(url_for("home"))

# ---------------- CREATE DB ----------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
