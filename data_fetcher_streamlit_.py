from db_utils_ import establish_connection_clickhouse_
from db_utils_ import import_data_from_clickhouse_ as fetch_data
import streamlit as st

def get_from_table_():
    clickhouse_client_ = establish_connection_clickhouse_.get_clickhouse_client_()
    # print('-- Data Fetcher Streamlit --- Got the client for clickhouse -- >> ', clickhouse_client_)
    tab_result  = fetch_data.fetch_all_rows_(clickhouse_client_)
    # print('-- Data Fetcher Streamlit --- Fetching table result done -- >> ', tab_result)
    return tab_result

# if __name__ == "__main__":  
#     tab_result = fetch_from_table_()
#     print(type(tab_result))
