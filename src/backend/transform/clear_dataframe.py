from backend.database.query import Connection_DB
from backend.extract.bookings_file import Excel
from backend.utils.credentials import DBConfig
import pandas as pd
from datetime import timedelta

def get_database():
    db_config = DBConfig().get_env_config()
    conn = Connection_DB(**db_config)
    return conn

def queries(query):
    return get_database().query(db_query= query)

def change_date(column):
    return column + timedelta(days=1)

def transform_df_date(column):
    return pd.to_datetime(column,dayfirst=True)

def transform_dataframe():
    excel = Excel().read_file()
    excel.columns = ['Data de pagamento', 'Descrição', 'Valor']
    excel['Status'] = 'Falso'
    excel['Data de pagamento'] = transform_df_date(excel['Data de pagamento'])
    excel['Data de pagamento'] = change_date(excel['Data de pagamento'])
    excel['Data de pagamento'] = excel['Data de pagamento'].dt.strftime('%Y-%m-%d')
    return excel.reset_index(drop=True)

def finish_date_clear(df):
    df['Data de pagamento'] = pd.to_datetime(df['Data de pagamento'])
    df['Data de pagamento'] = df['Data de pagamento'] - timedelta(days=1)
    return df
