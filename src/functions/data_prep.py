# Imports
import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
import pytz
from pycaret.regression import load_model

def initialize_data(data_path):
    """
    takes in files path and returns dataframes
    
    data_path: string: is already initialized in the app.py file
    """
    df = pd.read_csv(data_path)
    df["PayDate"] = pd.to_datetime(df["PayDate"], errors="coerce", utc=True)
    df_temp = df.dropna().drop(columns = ["PatNum"])[(df["PayDate"] > (dt.now(tz=pytz.UTC) - timedelta(days=3650))) & (df["PayDate"] < (dt.now(tz=pytz.UTC) - timedelta(days=130)))]
    df_temp = df_temp.groupby(pd.Grouper(key="PayDate", freq="1M")).sum()

    # this is taking the series and reshaping it into months as columns and years as rows
    s = pd.Series([2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020])
    new_df = pd.DataFrame(np.zeros(shape=(10,12)), columns = ["1","2","3","4","5","6","7","8","9","10","11","12"]).set_index([s])
    for i in range(len(df_temp)):
        new_df[str(df_temp.index[i].month)].loc[df_temp.index[i].year] = df_temp.iloc[i].values[0]
    new_df['Total'] = new_df.sum(axis=1)

    return df_temp, new_df

def initialize_model(model_path):
    """
    takes in file paths and returns model
    
    model_path: string: is already initialized in the app.py file
    """
    return load_model(model_path)
