from flask import *
 
app = Flask(__name__)

@app.route('/')
def method1():
  return " Welcome AIML Jan24 f1"

if __name__ == '__main__':
  app.run()