"""Model Prediction Interface"""
# import pickle
from io import StringIO
from flask import Flask, request, jsonify
import pandas as pd
import mlflow


# Option 1: Downloaded the model from S3 , to avoid issues during dockerization
#with open ('model.xgb','rb') as f_in:
    #model = pickle.load(f_in)


# Option 2: Automatic Download from S3 using MLflow, needs AWS credentials
RUN_ID = 'd47c2b1532f0499d82772b931fb9c30b'
logged_model = f's3://millproject-models/350780338872700929/{RUN_ID}/artifacts/model'
model = mlflow.pyfunc.load_model(logged_model)


def predict(features):
    """Predict Function"""
    preds = model.predict(features)
    return float(preds[0])

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
