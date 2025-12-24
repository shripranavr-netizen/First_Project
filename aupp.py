from flask import Flask, render_template, request
import mysql.connector as mysql

app = Flask(__name__)


mycon=mysql.connect(host="localhost",
                    user="root",
                    password="salt",
                    database="shan")
mycur=mycon.cursor()


def add_student(detail_list):
    query="INSERT INTO STUDENTS (name, age, course) VALUES (%s,%s,%s)"
    mycur.execute(query,detail_list)
    mycon.commit()

def view_student(name):
    query="SELECT * FROM STUDENTS WHERE NAME = %s;"
    mycur.execute(query,(name,))
    result=mycur.fetchone()
    return result


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add")
def form():
    return render_template("add_student.html")
   

@app.route("/submit",methods=["POST"])
def submit():
    stu_name=request.form["name"]
    stu_age=request.form["age"]
    stu_course=request.form["course"]
    add_student((stu_name,stu_age,stu_course))
    return "<h3>Student Added Successfully</h3><a href='/'>Home Page</a>"

@app.route("/view")
def view_page():
    return render_template("students.html")

@app.route("/view_result",methods=["POST"])
def view_result():
    s_name=request.form["name"] 
    data=view_student(s_name)
    return render_template("students.html",stu=data)

if __name__ == "__main__":
    app.run(debug=True)
