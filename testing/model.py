""" ML Workflow extracted from Mage Orchestration"""

import pickle
import pandas as pd
import numpy as np
from scipy import stats


def load_model():
    """Load the model extracted from S3 bucket"""
    with open('/home/nikki/MlOps_MillProject/testing/model.xgb','rb') as model_in:
        model_test = pickle.load(model_in)
    return model_test

class Model():
    """Model workflow template"""
    def __init__(self,model):
        self.model=model


    def prepare_features_datetime(self,df):
        """ Converting dates"""
        df['Date']= pd.to_datetime(df['Date'],format='mixed')
        return df


    def prepare_features_process(self,df):
        """Preprocessing features """
        df=df[df['Running Hour'] ==1]
        for lab,row in df.iterrows():
            if df.loc[lab,'Mill Outlet'] >= 0:
                df.loc[lab,'Mill Outlet']=row['Mill Outlet'] * -1

        return df

    def prepare_features_filter_merge(self,df1,df2):
        """Filtering and Merging Process and Quality Dataframe"""
        df2= df2[['Date','45um']]
        df1=df1[['Date','Limestone Feed Rate','Air Separator','Mill Outlet','Mill Outlet Temperature',\
        'Bucket Elevator' ,'Separator Inlet Damper' ,'Mill Dust Fan Damper','BM3 Main Drive']]
        df3=df2.merge(df1, on='Date', how='inner')
        df3.drop('Date',axis=1, inplace=True)
        df3.dropna(inplace=True)

        return df3

    def prepare_features_outlierhandling(self,df):
        """Outlier Handling"""
        z_scores =stats.zscore(df)
        abs_z_scores =np.abs(z_scores)
        #pylint: disable=redefined-builtin
        filter =(abs_z_scores <3).all(axis=1)
        dfz=df[filter]
        dfz=dfz[['Limestone Feed Rate','Air Separator','Mill Outlet','Mill Outlet Temperature', \
       'Bucket Elevator' ,'Separator Inlet Damper','BM3 Main Drive','Mill Dust Fan Damper']]
        
        return dfz
