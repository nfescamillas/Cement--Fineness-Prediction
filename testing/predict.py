"""Predict Function"""
import pickle
from io import StringIO
from flask import Flask, request, jsonify
import pandas as pd


with open ('model.xgb','rb') as f_in:
    model = pickle.load(f_in)

def predict(features):
    """Predict Function"""
    preds = model.predict(features)
    final_pred=pd.Series(preds).to_json(orient='values')
    return final_pred

app= Flask("fineness prediction")

@app.route('/predict',methods=['GET','POST'])
def predict_endpoint():
    """Predict End Point"""
    data = request.get_json()
    df=pd.read_json(StringIO(data))
    pred = predict(df.values)
    result ={"fineness": pred}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port =9696)
