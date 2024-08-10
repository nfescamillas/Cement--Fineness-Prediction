"""Integration Test"""

import sys
import requests
from deepdiff import DeepDiff
import pandas as pd


sys.path.insert(1, '/home/nikki/MlOps_MillProject/testing')

from model import Model
import model



model_pred= model.load_model()
model_service =Model(model_pred)

path ="/home/nikki/MlOps_MillProject/data/Mill_Data.xlsx"

dfp =pd.read_excel(path, sheet_name="Process_Data")
dfq =pd.read_excel(path,sheet_name="Quality_Data")

dfp=model_service.prepare_features_datetime(dfp)
dfq=model_service.prepare_features_datetime(dfq)
dfp=model_service.prepare_features_process(dfp)
dff=model_service.prepare_features_filter_merge(dfp[0:5],dfq[0:5])
dfz=model_service.prepare_features_outlierhandling(dff)


exp_response =model_service.model.predict(dfz)
actual_df = pd.Series(exp_response)
actual_df =actual_df.to_json(orient='values')
actual={'fineness': actual_df}


dfj =dfz.to_json(orient='values')
url ="http://localhost:9696/predict"
response =requests.post(url,json=dfj,timeout=60)
expected =response.json()

diff =DeepDiff(actual,expected)
print(diff)
