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
@app.route('/adduserdata1',methods=['POST'])
def adduserdata1():
  
  name=(request.form.get("name"))
  
  
  ##database vala kaam 

  con  = sqlite3.connect("myDB")  # connect sms database 
  con.row_factory = sqlite3.Row  # create object of Row 
  cur = con.cursor()             # create cursor object, which will hold records 
  
  insql="insert into attendance(name,date_time) values ('"+name+"',datetime('now', '+5 hours', '+30 minutes'))"
  cur.execute(insql) 
  con.commit() 
  con.close()
  msg="Welcome To Predictor"
  return render_template('index.html',pprice=pp)


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