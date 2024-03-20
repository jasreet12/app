from flask import *
 
app = Flask(__name__)
###########
file = "https://github.com/sarwansingh/Python/blob/master/ClassExamples/data/Bengaluru_House_Data_clean.csv"


###########

@app.route('/')
def method1():
  return render_template("index.html")
  # return " Welcome AIML Jan24 f1"
@app.route('/contact')
def method_contact():
  return render_template("contact.html")

if __name__ == '__main__':
  app.run()