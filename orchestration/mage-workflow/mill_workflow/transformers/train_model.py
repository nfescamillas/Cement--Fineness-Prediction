from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
import numpy as np 
import xgboost as xgb


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
    X = data[['Limestone Feed Rate','Air Separator','Mill Outlet','Mill Outlet Temperature', 'Bucket Elevator' ,'Separator Inlet Damper' \
     ,'BM3 Main Drive','Mill Dust Fan Damper']]
    y= data['45um']
    X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.3)
    xg_reg =xgb.XGBRegressor()

    
    params_grid={'max_depth': [3, 4, 5, 7,9],
        'n_estimators' :[50,75,100,150,200],
        'min_child_weight': np.arange(0.0001, 0.5, 0.001),
        'gamma': np.arange(0.0,40.0,0.005),
        'learning_rate': np.arange(0.0005,0.3,0.0005),
        'subsample': np.arange(0.01,1.0,0.01),
        'colsample_bylevel': np.round(np.arange(0.1,1.0,0.01)),
        'colsample_bytree': np.arange(0.1,1.0,0.01)}

    xg_randsearch =RandomizedSearchCV(estimator =xg_reg, param_distributions=params_grid,n_iter=500,scoring='neg_mean_squared_error',cv=10,verbose=1)
    xg_randsearch.fit(X_train.values,y_train.values)

    xg_best_score =xg_randsearch.best_score_
    xg_best_params =xg_randsearch.best_params_

    return xg_randsearch,X,y,xg_best_params,xg_best_score

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
