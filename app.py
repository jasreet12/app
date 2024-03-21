from flask import *
import pandas as pd 
import numpy as np 
from sklearn.linear_model import LinearRegression

app = Flask(_name_)
##############
file ="https://raw.githubusercontent.com/sarwansingh/Python/master/ClassExamples/data/Bengaluru_House_Data_clean.csv"
df = pd.read_csv(file)
X = df.drop(['Unnamed: 0' ,'price'], axis='columns')
Y = df.price

lrmodel = LinearRegression()
lrmodel.fit(X,Y)
def predictprice(location,sqft,bath,bhk):
    '''
    Function which helps to actually predict the prices.
    '''
    loc_index = np.where(X.columns==location)[0][0]     # np.where() function returns the indices of elements in an input array where the given condition is satisfied.

    x = np.zeros(len(X.columns))    # np.zeros() function returns a new array of given shape and type, with zeros.
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
  return render_template("project.html")

@app.route('/predict' ,methods =["POST"] )
def methodpredict():
  loc   = request.form.get("loc")  #'Kothanur'
  sqft  = request.form.get("size")
  bhk   = request.form.get("bhk")
  bath  = request.form.get("bath")
  pp = predictprice(loc, sqft, bhk, bath).round(3)
  return render_template("project.html", pprice=pp)

@app.route('/contact')
def methodcontact():
  return render_template("contact.html")

# return " Welcome AIML Jan24 f1"

if _name_ == '_main_':
  app.run()