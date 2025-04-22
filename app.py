"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""




from flask import Flask,render_template,request,redirect,url_for,flash
from flask_login import LoginManager,UserMixin, login_required, login_user, current_user,logout_user
import sqlite3
from flask_bcrypt import Bcrypt, bcrypt


app = Flask(__name__)
bcrypt=Bcrypt(app)

app.config['SECRET_KEY']='thisIsSecret'
login_manager=LoginManager(app)
login_manager.login_view = "login"

#create a user model represent ing and user 
class User(UserMixin):
    def __init__(self,id,email,password):
        self.id=id
        self.email=email
        self.password=password
        self.authenticated=False
        def is_active(self):
            return self.is_active()
        def is_anonymous(self):
            return False
        def is_authenticated(self):
            return self.authenticated
        def is_active(self):
            return True
        def get_id(self):
            return self.id


@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
        #check if alredy logged in- if so send home
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        #do the standart stuff and find the user with email
        con=sqlite3.connect("login.db")
        curs=con.cursor()
        email=request.form['email']
        curs.execute("SELECT * FROM tblLogin WHERE email = (?)", [email])
        #return the first matching user then pass the details to 
        #create user object - unless there is nothingreturned then flash a message
        row=curs.fetchone()
        if row==None:
            flash('Please try logging in again')
            return render_template('login.html')
        user= list(row)
        liUser=User(int(user[0]),user[1],user[2])
        password = request.form['password']
        # Use bcrypt to check password
        match = bcrypt.check_password_hash(liUser.password, password)
        #if our password matches- run the login_user method
        if match and email==liUser.email:
            login_user(liUser,remember = request.form.get('remember'))
            redirect(url_for('home'))
        else:
            flash('Please try logging in again')
            return render_template('login.html')
        return render_template('home.html')

@login_manager.user_loader
def load_user(user_id):
    conn=sqlite3.connect('login.db')
    curs =conn.cursor()
    curs.execute("SELECT * FROM tblLogin WHERE userID=(?)", [user_id])
    liUser =curs.fetchone()
    if liUser is None:
        return None
    else:
        return User(int(liUser[0]), liUser[1],liUser[2])

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register_post():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    con=sqlite3.connect("login.db")
    curs= con.cursor()
    email=request.form['email']
    password= request.form['password']
    #we use bycrpt to hash the password we've put in with salt
    hashedPassword=bcrypt.generate_password_hash(password)
    #now add that to database
    con.execute('INSERT INTO tblLogin (email, password) VALUES (?,?)',[email,hashedPassword])
    con.commit()
    return render_template('home.html')





@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
@login_required
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            name= request.form['name']
            addr= request.form['address']
            city= request.form['city']
            with sqlite3.connect("student.db") as con:
                cur=con.cursor()
                cur.execute("INSERT INTO tblStudent (StudentID,FirstName,Address,City) VALUES (NULL,?,?,?)", (name,addr,city))
                con.commit()
                msg="Record successfully added"
        except:
            con.rollback()
            msg= "Error in insert operation"
        finally:
            con.close()
            return render_template("result.html", msg=msg)

@app.route('/liststudents')
@login_required
def listStudents():
    con=sqlite3.connect("student.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from tblStudent")

    rows=cur.fetchall();
    return render_template ("studentlist.html", rows=rows)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
app.debug=True
app.run()
