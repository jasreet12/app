from flask import *
import pandas as pd 
import numpy as np 
from sklearn.linear_model import LinearRegression
import sqlite3
from flask import request
from datetime import datetime

app = Flask(__name__)


def create_database():
  # Connect to the SQLite database (or create it if it doesn't exist)
  conn = sqlite3.connect('myDB')

    # Create a cursor object to execute SQL commands
  cur = conn.cursor()

    # Define SQL commands to create tables
  cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
  # Fetch all table names
  tables = cur.fetchall()

  # Print table names
  print("Tables in the database:")
  for table in tables:
      print(table[0])
    

  # Close the connection
  conn.close()
# create_database()




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
    con = sqlite3.connect("myDB")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT id,name, strftime('%Y-%m-%d %H:%M:%S', date_time) AS formatted_date_time FROM attendance")
    rows = cur.fetchall()
    rows_with_serial = [(idx + 1, row['name'], row['formatted_date_time']) for idx, row in enumerate(rows)]
    con.close()
    return render_template("showData.html", data=rows_with_serial)

######





@app.route('/adduserdata1', methods=['get'])  # Specify that this route handles POST requests
def adduserdata1():
    name = request.form.get("name")
    con = sqlite3.connect("myDB")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()             
  
    insql = "INSERT INTO attendance(name, date_time) VALUES (?, datetime('now', '+5 hours', '+30 minutes'))"
    cur.execute(insql, (name,))
    con.commit() 
    con.close()
  
    return render_template('index.html')



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
  pp = predictprice(loc, sqft, bath, bhk).round(3)
  return render_template("project.html", pprice=pp ,locations = df.columns[5:] )




@app.route('/contact')
def methodcontact():
  return render_template("contact.html")



@app.route('/getlocation')
def methodLocation():
  return render_template("getLocation.html")



# return " Welcome AIML Jan24 f1"

if __name__ == '__main__':
  app.run()