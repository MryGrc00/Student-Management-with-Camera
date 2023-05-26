from flask import Flask,render_template,request,redirect,flash,session
from dbhelper import *

app = Flask(__name__)
app.secret_key="@@#$Grace@#"

upload_folder='static/images'
app.config['UPLOAD_FOLDER']=upload_folder


@app.route("/upload",methods=['POST','GET'])
def upload():
    file = request.files['webcam']
    idno: str = request.args.get('idno')
    lastname: str = request.args.get('lastname')
    firstname: str = request.args.get('firstname')
    course: str = request.args.get('course')
    level: str = request.args.get('level')
    imagename: str = idno+".png"
    
    file.save(upload_folder+"/"+imagename) #get the image upload to server and store to upload folder
    #if idno!='' and lastname!='' and firstname!='':
    okey: int = addrecord('student',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level,image=imagename)
    return redirect("/main")
    
@app.route("/register")
def register():
    return render_template("/register.html",headername='register student')

@app.route("/deletestudent",methods=["GET"])
def deletestudent():
    idnumber: str = request.args.get("idno")
    okey: int = deleterecord('student',idno=idnumber)
    if okey>0:
        flash("Student Deleted !!")
        return redirect("/main")
    else:
        flash("Error Deleting Student !!")
        return redirect("/main")

@app.route("/savestudent",methods=["POST"])
def savestudent():
    idno: str = request.form["idno"]
    lastname: str = request.form["lastname"]
    firstname: str = request.form["firstname"]
    course: str = request.form["course"]
    level: str = request.form["level"]
    flag: str = request.form["flag"]
    #validate
    if idno!="" and lastname!="" and firstname!="":
        if flag=="0":        
            okey: int = addrecord('student',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level)
            if okey>0:
                flash("New Student Added")
                return redirect("/main")
        else:
            okey: int = updaterecord('student',idno=idno,lastname=lastname,firstname=firstname,course=course,level=level)
            if okey>0:
                flash("Student Information Updated")
                return redirect("/main")
    else:
        flash("Fill All Fields !")
        return redirect("/main")
            
@app.after_request
def after_request(response):
    response.headers["Cache-Control"]="no-cache,no-store,must-revalidate"
    return response

@app.route("/logout")
def logout():
    session.clear()
    flash("Your are logged out!")
    return redirect("/")

@app.route("/main")
def main():
    if "logged_user" in session:
        header: list = ['idno','lastname','firstname','course','level','action']
        slist: list = getallrecord('student')
        return render_template("main.html",headername='students',studentlist=slist,head=header)
    else:
        flash("Login Properly !!")
        return redirect("/")
        
@app.route("/login",methods=['POST'])
def login():
    uname: str = request.form["username"]
    pword: str = request.form["password"]
    user: dict = userlogin('users',username=uname,password=pword)
    if user != None:
        session["logged_user"]=uname
        flash("Login Accepted")
        return redirect("/main")
    else:
        flash("Login Failed")
        return redirect("/")

@app.route("/")
def index():
    return render_template("login.html",headername='welcome')

if __name__=="__main__":
    app.run(debug=True)