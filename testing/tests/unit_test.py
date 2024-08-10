""" Module for unit testing code"""
import pickle
from pandas.api.types import is_datetime64_any_dtype
import pandas as pd
import numpy as np
from scipy import stats
from model import Model

dfp =pd.read_excel("/home/nikki/MlOps_MillProject/data/Mill_Data.xlsx", sheet_name="Process_Data")
dfq =pd.read_excel("/home/nikki/MlOps_MillProject/data/Mill_Data.xlsx",sheet_name="Quality_Data")

def load_model():
    """Load the model extracted from S3 bucket"""
    with open('model.xgb','rb') as model_in:
        model_test = pickle.load(model_in)
    return model_test

model_pred= load_model()

model_service =Model(model_pred)

df1 =model_service.prepare_features_datetime(dfp)
df2 =model_service.prepare_features_datetime(dfq)

def test_prepare_features_date():
    """ Converting dates
    """
    assert (is_datetime64_any_dtype(df1['Date']))  &  (is_datetime64_any_dtype(df2['Date']))

df1 =model_service.prepare_features_process(df1)

def test_prepare_features_process():
    """ Processing inputs for process data
    """
    expected_value = 1
    assert (df1['Running Hour'].mean() == expected_value)  &  (df1['Mill Outlet'].min() < 0)

df3 =model_service.prepare_features_filter_merge(df1,df2)


def test_prepare_features_filter_merge():
    """ Filtering and Merging dataframes on Date
    """
    expected_value = 9
    assert ('Date' not in  df3.columns) &  (df3.isna().values.sum() == 0 ) \
        &  (len(df3.columns) == expected_value)

dfz = model_service.prepare_features_outlierhandling(df3)

def test_prepare_features_outlierhandling():
    """ Outlier Handling using 3 sigma rule 
    """
    z_scores =stats.zscore(dfz)
    abs_z_scores =np.abs(z_scores)
    #pylint: disable=redefined-builtin
    filter =(abs_z_scores >3).all(axis=1)
    dfzt=dfz[filter]
    assert len(dfzt) == 0



def test_model_predict():
    """ Predicting using model downloaded from S3
    """
    preds =model_service.model.predict(dfz)
    assert preds is not None
