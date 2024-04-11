from flask import *
import pandas as pd 
import numpy as np 
from sklearn.linear_model import LinearRegression
import sqlite3

app = Flask(__name__)
##############
file ="https://raw.githubusercontent.com/sarwansingh/Python/master/ClassExamples/data/Bengaluru_House_Data_clean.csv"
df = pd.read_csv(file)
X = df.drop(['Unnamed: 0' ,'price'], axis='columns')
Y = df.price

lrmodel = LinearRegression()
lrmodel.fit(X,Y)
######### get all locations in the list
# collist = df.columns
# loclist = []
# for item in collist[5:] : 
# # print (" <option> " + item + "</option>")
# loclist.append( " <option> " + item + "</option>" )
##################



@app.route('/showdata')
def showdata():
  con  = sqlite3.connect("myDB")  # connect sms database
  con.row_factory = sqlite3.Row  # create object of Row
  cur = con.cursor()             # create cursor object, which will hold records 
                      # being fetched from database. 
 
  cur.execute( "select * from users") 
  rows = cur.fetchall()          # all the data pulled from database is stored in rows object 
  con.close ()
  return render_template("showdata.html", data=rows) 

###
@app.route('/signup')
def signup():
  
  
  return render_template("signup.html")

####

 
  
  
  SQLite format 3@  -�
PV�P^!!�tableattendanceattendanceCREATE TABLE attendance (name varchar(50),date_time DATETIME)Rytablestudent1student1CREATE TABLE student1( name varchar,datetime DATETIME)P++Ytablesqlite_sequencesqlite_sequenceCREATE TABLE sqlite_sequence(name,seq)�'�%tablestudentstudentCREATE TABLE student(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name varchar(50),
username varchar(50),
email varchar(50),
passowrd varchar(50))
	&��{<���X&0	-#RAGHAVRAGHAV222RAGHAV@gmail.comhuggingface6#1#AMANDEEPAMANDEEP222AMANDEEP@gmail.comhuggingface0-#RAGHAVRAGHAV222RAGHAV@gmail.comhuggingface;)7!Prateek MittalPrateekCPrateekm201@gmail.comprateek201;)7!Prateek MittalPrateekCPrateekm201@gmail.comprateek201=-?AmandeepcooldudeAmandeepdubeyamandeep72@gmail.combhagya#-Rakeshrakrakesh@gmail.comrara,--Ridham Khazanchiridzridham@gmail.comrk0%7Raghav Batraraghavbraghavb4563@gmail.comrr
��student	


z����jK-����z
3PRANJAL2024-04-10 15:40:573RAGHAV2024-04-10 15:31:193RAGHAV2024-04-10 15:30:39
3RAGHAV2024-04-10 15:18:23	3MANYA2024-04-10 15:14:063MANYA2024-04-10 15:09:593RAGHAV2024-04-10 14:55:213ANUBHAV2024-04-10 14:48:323Unknown2024-04-10 14:46:173RAGHAV2024-04-10 14:42:003AMANDEEP2024-04-10 14:44:543RAGHAV2024-04-10 09:00:453abc2024-04-10 08:57:25
  

@app.route('/adduserdata',methods=['POST'])
def adduserdata():
  username=(request.form.get("username"))
  name=(request.form.get("name"))
  email=(request.form.get("email"))
  password=(request.form.get("upassword"))
  
  ##database vala kaam 

  con  = sqlite3.connect("myDB")  # connect sms database 
  con.row_factory = sqlite3.Row  # create object of Row 
  cur = con.cursor()             # create cursor object, which will hold records  
  insql="insert into student(name,username,email,passowrd) values ('"+name+"' , '"+username+"' , '"+email+"' , '"+password+"')"
  cur.execute(insql) 
  con.commit() 
  con.close()
  date = datetime.now()
  msg="Welcome To Predictor"
  return render_template('index.html',a=date)

####
@app.route('/login')
def login():
  return render_template("login.html")


@app.route("/loginuser",methods=['POST'])
def loginuser():
  usern=(request.form.get("username"))
  pw=(request.form.get("pwd"))
  # connect with database and check whether record 
  # exist with username having email as uemail and password as upwd.
  con  = sqlite3.connect("myDB") 
  con.row_factory = sqlite3.Row
  cur = con.cursor() 
  cur.execute( "select * from student where username=='%s' and passowrd=='%s'" %(usern, pw ))
  rows = cur.fetchall()
  con.close ()
  uname =""
  for r in rows :
    uname  = r["username"]
    
  if uname is ""  :
    msg="Invalid user"
    return   render_template('login.html',a=msg) #str(" Invalid user ")
  else :
    session ["username"] = uname
    msg="Welcome back "+r["name"]
  return render_template('index.html',a=msg)


  
@app.route('/logout')
def logout():
  #remove session varible and redirect to index page
  session.clear()  # will clear the entire session 
  #session.pop("username")  # will remove only one variable named username 
  return redirect( url_for('method1'))







@app.route('/adduserdata1',methods=['POST'])
def adduserdata1():
  
  name=(request.form.get("name"))
  

  con  = sqlite3.connect("myDB")  # connect sms database 
  con.row_factory = sqlite3.Row  # create object of Row 
  cur = con.cursor()             # create cursor object, which will hold records 
  
  insql="insert into attendance(name,date_time) values ('"+name+"',datetime('now', '+5 hours', '+30 minutes'))"
  cur.execute(insql) 
  con.commit() 
  con.close()
  msg="Welcome To Predictor"
  return render_template('index.html',pprice=msg)




def predictprice(location,sqft,bath,bhk):
  '''
  Function which helps to actually predict the prices.
  '''
  loc_index = np.where(X.columns==location)[0][0] # np.where() function returns the indices of elements in an input array where the given condition is satisfied.

  x = np.zeros(len(X.columns)) # np.zeros() function returns a new array of given shape and type, with zeros.
  x[0] = sqft
  x[1] = bath
  x[2] = bhk
  if loc_index >= 0:
    x[loc_index] = 1

  return lrmodel.predict([x])[0]
############

@app.route('/')
def method1():

  return render_template("index.html" )


@app.route('/project')
def methodproject():
  return render_template("project.html" , locations = df.columns[5:])

@app.route('/predict' ,methods =["POST"] )
def methodpredict():
  loc = request.form.get("loc") #'Kothanur'
  sqft = request.form.get("size")
  bhk = request.form.get("bhk")
  bath = request.form.get("bath")
  pp = predictprice(loc, sqft, bhk, bath).round(3)
  return render_template("project.html", pprice=pp)

@app.route('/contact')

def methodcontact():
  return render_template("contact.html")

# return " Welcome AIML Jan24 f1"

if __name__ == '__main__':
  app.run()