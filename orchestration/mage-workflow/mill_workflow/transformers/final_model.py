from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np 
import xgboost as xgb
import mlflow
import os


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    

    os.environ["AWS_ACCESS_KEY_ID"] =  "{{ env_var('AWS_ACCESS_KEY_ID') }}"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "{{ env_var('AWS_SECRET_ACCESS_KEY') }}"
    


    remote_server_uri ="http://ec2-52-90-86-18.compute-1.amazonaws.com:5000/"
    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment('Mill Fineness Project')
    
    
    with mlflow.start_run():
        params = data[3]
        mlflow.log_params(params)
        X_train,X_test,y_train,y_test= train_test_split(data[1],data[2],test_size=0.3,)
        xg_final =xgb.XGBRegressor(**params).fit(X_train.values,y_train.values)
        y_pred=xg_final.predict(X_test.values)
        rmse=np.sqrt(mean_squared_error(y_test,y_pred))
        mlflow.log_metric('rmse', rmse)
        
        mlflow.xgboost.log_model(xg_final,artifact_path ="model")

    return xg_final,rmse

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
