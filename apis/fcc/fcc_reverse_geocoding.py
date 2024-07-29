from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
from get_FIPS_2020census import get_FIPS
import os
from filecmp import cmpfiles
import time

op_kwargs={"locations_dir" : r"/home/ubuntu/iNaturalist/Location_csvs",
        "save_dir" : r"/home/ubuntu/iNaturalist/FIPS_output"}

def find_csv(**kwargs):
    """
    Matches location and save dir to 
    determine which csv to process next
    from locations_dir                         
    """
    loc = kwargs['dirs']['locations_dir']
    save = kwargs['dirs']['save_dir']
    source = os.listdir(loc)
    target = os.listdir(save)
    if target == []:
        print("Save Directory is empty! Seleting first file in locations_dir") 
        next_csv = kwargs['ti'].xcom_push(key="next_csv", value=os.path.join(loc,source[0]))
        return 0
    
    if source == target:
        print("All directories succesfully processed, no more runs required")
        return 1
    
    # compares files in locations and save
    # mismatch files have the same name but different contents
    # error files are those which are in locations_dir but not save_dir
    _, mismatch, error = cmpfiles(loc,save, source)
    next_csv = error[0]
    print("Next csv has been found!")
    next_csv = kwargs['ti'].xcom_push(key="next_csv", value=os.path.join(loc,next_csv))
    return 0

def get_FIPS_fromCSV(**kwargs):
    """
    Get FIPS and other census data
    based on latitude and longitude
    coorinates
    """
    #make task_ids part of kwargs so we can reuse this function
    next_csv = kwargs['ti'].xcom_pull(key="next_csv", task_ids=kwargs['find_id'])
    csv_name = os.path.basename(next_csv)
    save_path = os.path.join(kwargs['dirs']['save_dir'],csv_name)
    
    get_FIPS(next_csv, save_path)
    return 0

def sleeping_function(**kwargs):
    """ this function sleeps for a given time in minutes"""
    minutes = int(kwargs['sleep_time']) * 60
    time.sleep(minutes)

with DAG(
    "FCC_reverseGeocoding",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    find_csv_1 = PythonOperator(
        task_id="find_csv_1", python_callable=find_csv,
        op_kwargs={ 'dirs' : op_kwargs, 'find_id' : []}
        )
    
    find_csv_2 = PythonOperator(
        task_id="find_csv_2", python_callable=find_csv,
        op_kwargs={ 'dirs' : op_kwargs, 'find_id' : []}
        )
    
    find_csv_3 = PythonOperator(
        task_id="find_csv_3", python_callable=find_csv,
        op_kwargs={ 'dirs' : op_kwargs, 'find_id' : []}
        )
    
    find_csv_4 = PythonOperator(
        task_id="find_csv_4", python_callable=find_csv,
        op_kwargs={ 'dirs' : op_kwargs, 'find_id' : []}
        )
    
    api_request_1 = PythonOperator(
        task_id="api_request_1", python_callable=get_FIPS_fromCSV,
        op_kwargs={ 'dirs' : op_kwargs, 'find_id' : 'find_csv_1'}
    )
    
    api_request_2 = PythonOperator(
        task_id="api_request_2", python_callable=get_FIPS_fromCSV,
        op_kwargs={ 'dirs' : op_kwargs, 'find_id' : 'find_csv_2'}
    )
    
    api_request_3 = PythonOperator(
        task_id="api_request_3", python_callable=get_FIPS_fromCSV,
        op_kwargs={ 'dirs' : op_kwargs, 'find_id' : 'find_csv_3'}
    )
    
    api_request_4 = PythonOperator(
        task_id="api_request_4", python_callable=get_FIPS_fromCSV,
        op_kwargs={ 'dirs' : op_kwargs, 'find_id' : 'find_csv_4'}
    )
    
    t90 = PythonOperator(
        task_id="waited_090_min", python_callable=sleeping_function,
        op_kwargs = {'sleep_time' : '90'}
    )
    t180 = PythonOperator(
        task_id="waited_180_min", python_callable=sleeping_function,
        op_kwargs = {'sleep_time' : '90'}
    )
    t270 = PythonOperator(
        task_id="waited_270_min", python_callable=sleeping_function,
        op_kwargs = {'sleep_time' : '90'}
    )

find_csv_1 >> api_request_1 >> t90 >> find_csv_2 >> api_request_2 >> t180 >> find_csv_3 >> api_request_3 >> t270 >> find_csv_4 >> api_request_4
