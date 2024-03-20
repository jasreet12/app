from flask import *
 
app = Flask(__name__)

@app.route('/')
def method1():
  return render_template("index.html")
  # return " Welcome AIML Jan24 f1"
@app.route('/contact')
def method_contact():
  return render_template("contact.html")

if __name__ == '__main__':
  app.run()