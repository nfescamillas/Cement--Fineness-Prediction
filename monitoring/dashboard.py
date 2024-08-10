
import pandas as pd
import psycopg
from prefect import task, flow
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric,RegressionQualityMetric


create_table = """ drop table if exists monitoring_metrics;
create table monitoring_metrics(
    Date timestamp,
    prediction_drift float,
	reference_data_rmse float,
	current_data_rmse float)
"""

reference_data =pd.read_parquet("previous.parquet")
current_data =pd.read_parquet("current.parquet")

numerical_features=['Limestone Feed Rate', 'Air Separator', 'Mill Outlet',
       'Mill Outlet Temperature', 'Bucket Elevator', 'Separator Inlet Damper',
       'BM3 Main Drive', 'Mill Dust Fan Damper']

column_mapping =ColumnMapping(target ='45um', prediction ='prediction', numerical_features= numerical_features)


report= Report(metrics=[ColumnDriftMetric(column_name='prediction'),
                        RegressionQualityMetric(), 
                       ])

@task
def prep_db():
    with psycopg.connect("host=localhost port=5433 user=postgres password=admin", autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("create database test;")
        with psycopg.connect("host=localhost port=5433 dbname=test user=postgres password=admin") as conn:
            conn.execute(create_table)




@task
def calculate_metrics(curr):
    for index, row in current_data.iterrows():
        recent_data = current_data.loc[index,:]
        date= row['Date']
        final_data= pd.DataFrame(recent_data).transpose()
        report.run(reference_data = reference_data, current_data = final_data, column_mapping=column_mapping)
        result = report.as_dict()
        drift_score =result['metrics'][0]['result']['drift_score']
        ref_rmse =result['metrics'][1]['result']['reference']['rmse']
        cur_rmse =result['metrics'][1]['result']['current']['rmse']
        curr.execute(
			"insert into monitoring_metrics(date,prediction_drift, reference_data_rmse,current_data_rmse) values (%s, %s, %s, %s)",
			(date,drift_score,ref_rmse,cur_rmse)
    
        )

@flow
def main():
    prep_db() 
    with psycopg.connect("host=localhost port=5433 dbname=test  user=postgres  password=admin", autocommit=True) as conn:
        with conn.cursor() as curr:
            calculate_metrics(curr)



if __name__ == '__main__':
    main()
