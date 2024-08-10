"""Testing Model Prediction Interface"""
import requests
import pandas as pd

features =[{'Limestone Feed Rate':4.0,
           'Air Separator': 25.0,
           'Mill Outlet':-11.0,
           'Mill Outlet Temperature':95.0,
           'Bucket Elevator':25.0,
           'Separator Inlet Damper':82.0,
           'BM3 Main Drive':260.0,
           'Mill Dust Fan Damper':65.0}]


df = pd.DataFrame(features)
dff= df.to_json(orient='records')

#Option 1:  When deployed to elastic beanstalk, replace url with the app url
URL='fineness-prediction-env.eba-vk4atbw8.us-east-1.elasticbeanstalk.com'
url =f'http://{URL}/predict'

#Option 2 : Using localhost to send request
#url ="http://localhost:9696/predict"

response =requests.post(url,json=dff,timeout=60)
print(response.json())
