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

# ---------------- CREATE DB ----------------
with app.app_context():
    db.create_all()

# ---------------- HOME ----------------
@app.route("/")
def index():
    students = Student.query.all()
    teachers = Teacher.query.all()
    return render_template(
        "index.html",
        students=students,
        teachers=teachers
    )

# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")

    if User.query.filter_by(email=email).first():
        return "Email already registered ❌"

    user = User(
        fname=request.form.get("fname"),
        lname=request.form.get("lname"),
        email=email,
        password=request.form.get("password"),
        role=request.form.get("role")
    )

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("index"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(
        email=email,
        password=password
    ).first()

    if user:
        return "Login Successful ✅"
    return "Invalid Login ❌"

# ---------------- ADD STUDENT ----------------
@app.route("/add_student", methods=["POST"])
def add_student():
    s = Student(
        name=request.form.get("name"),
        email=request.form.get("email"),
        age=int(request.form.get("age")),
        student_class=request.form.get("class")
    )

    db.session.add(s)
    db.session.commit()

    return redirect(url_for("index"))

# ---------------- ADD TEACHER ----------------
@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    exp = request.form.get("experience")

    t = Teacher(
        name=request.form.get("name"),
        subject=request.form.get("subject"),
        age=int(request.form.get("age")),
        experience=int(exp) if exp else 0
    )

    db.session.add(t)
    db.session.commit()

    return redirect(url_for("index"))

# ---------------- EDIT STUDENT ----------------
@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form.get("name")
        student.email = request.form.get("email")
        student.age = int(request.form.get("age"))
        student.student_class = request.form.get("class")

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_student.html", student=student)

# ---------------- DELETE STUDENT ----------------
@app.route("/delete_student/<int:id>")
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return redirect(url_for("index"))

# ---------------- EDIT TEACHER ----------------
@app.route("/edit_teacher/<int:id>", methods=["GET","POST"])
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)

    if request.method == "POST":
        teacher.name = request.form.get("name")
        teacher.subject = request.form.get("subject")
        teacher.age = int(request.form.get("age"))
        teacher.experience = int(request.form.get("experience"))

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit_teacher.html", teacher=teacher)

# ---------------- DELETE TEACHER ----------------
@app.route("/delete_teacher/<int:id>")
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)

    db.session.delete(teacher)
    db.session.commit()

    return redirect(url_for("index"))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
