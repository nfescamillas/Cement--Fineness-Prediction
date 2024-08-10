import pandas as pd
import numpy as np
from scipy import stats

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(dfp,dfq, *args, **kwargs):
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
    
    dfp['Date']= pd.to_datetime(dfp['Date'])
    dfq['Date']= pd.to_datetime(dfq['Date'])
    dfp=dfp[dfp['Running Hour'] ==1]

    for lab,row in dfp.iterrows():
        if dfp.loc[lab,'Mill Outlet'] >= 0:
            dfp.loc[lab,'Mill Outlet']=row['Mill Outlet'] * -1

    dfq= dfq[['Date','45um']]
    dfp=dfp[['Date','Limestone Feed Rate','Air Separator','Mill Outlet','Mill Outlet Temperature', 'Bucket Elevator' ,'Separator Inlet Damper' \
     ,'Mill Dust Fan Damper','BM3 Main Drive']]

    dff=dfq.merge(dfp, on='Date', how='inner')
    dff.drop('Date',axis=1, inplace=True)
    dff.dropna(inplace=True)

    z_scores =stats.zscore(dff)
    abs_z_scores =np.abs(z_scores)
    filter =(abs_z_scores <3).all(axis=1)
    dfz=dff[filter]
    
    
    
    return dfz


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
