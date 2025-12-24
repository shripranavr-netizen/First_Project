from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Your Firebase Realtime Database URL
FIREBASE_URL = 'https://project-26405-default-rtdb.firebaseio.com/'

def add_student(name, age, course):
    try:
        # POST request to add student
        url = f"{FIREBASE_URL}/STUDENTS.json"
        data = {
            "name": name,
            "age": age,
            "course": course
        }
        response = requests.post(url, json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error adding student: {e}")
        return False

def view_student(name):
    try:
        # GET request to fetch all students
        url = f"{FIREBASE_URL}/STUDENTS.json"
        response = requests.get(url)
        
        if response.status_code == 200:
            students = response.json()
            if students:
                for key, value in students.items():
                    if value.get("name") == name:
                        return value
        return None
    except Exception as e:
        print(f"Error viewing student: {e}")
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add")
def form():
    return render_template("add_student.html")

@app.route("/submit", methods=["POST"])
def submit():
    stu_name = request.form["name"]
    stu_age = request.form["age"]
    stu_course = request.form["course"]
    
    # Fixed: Pass arguments separately, not as tuple
    add_student(stu_name, stu_age, stu_course)
    
    return "<h3>Student Added Successfully</h3><a href='/'>Home Page</a>"

@app.route("/view")
def view_page():
    return render_template("students.html")

@app.route("/view_result", methods=["POST"])
def view_result():
    s_name = request.form["name"]
    data = view_student(s_name)
    return render_template("students.html", stu=data)

if __name__ == "__main__":
    app.run(debug=True)