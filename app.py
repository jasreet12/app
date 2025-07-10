from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# 📦 Load & Train Model
file = "https://raw.githubusercontent.com/sarwansingh/Python/master/ClassExamples/data/Bengaluru_House_Data_clean.csv"
df = pd.read_csv(file)

X = df.drop(['Unnamed: 0', 'price'], axis=1)
y = df['price']

lrmodel = LinearRegression()
lrmodel.fit(X, y)

# 🧠 Prediction Function
def predict_price(location, sqft, bath, bhk):
    try:
        loc_index = np.where(X.columns == location)[0][0]
    except:
        loc_index = -1

    x = np.zeros(len(X.columns))
    x[0] = float(sqft)
    x[1] = float(bath)
    x[2] = float(bhk)

    if loc_index >= 0:
        x[loc_index] = 1

    return round(lrmodel.predict([x])[0], 3)

# 🔹 Home Page
@app.route('/')
def home():
    return render_template("index.html", locations=X.columns[3:], pprice=None)

# 🔹 Predict Route
@app.route('/predict', methods=["POST"])
def predict():
    loc = request.form.get("loc")
    sqft = request.form.get("size")
    bhk = request.form.get("bhk")
    bath = request.form.get("bath")
    predicted_price = predict_price(loc, sqft, bath, bhk)
    return render_template("index.html", pprice=predicted_price, locations=X.columns[3:])

# ▶️ Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
