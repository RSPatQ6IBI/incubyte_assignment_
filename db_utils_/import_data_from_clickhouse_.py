import clickhouse_connect
from db_utils_.establish_connection_clickhouse_ import get_clickhouse_client_
import db_utils_.db_commands_ as db_commands_
import tomllib
from pathlib import Path

def get_clickhouse_client_():
    a_clickhouse_client_ = get_clickhouse_client_()
    return a_clickhouse_client_

def fetch_all_rows_(a_client_):
    parent_dir = Path(__file__).resolve().parent.parent
    config_path = str(parent_dir / "pyproject.toml")
    config_path = config_path.replace("\\", "/")
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    tab_name_ = data["clickhouse-db"]["table_name_"]   # Nested entries (tables)
    fetch_data_query_ = db_commands_.fetch_all_entries_from_table(table_name_=tab_name_)
    # print(' DATA QUERY --- >> ',fetch_data_query_)
    tab_result = a_client_.query_df(fetch_data_query_)
    # print('Tab Result Set --- >>> ',tab_result)
    return tab_result

# if __name__ == "__main__":
    # the_clickhouse_client_ = get_clickhouse_client_()  
    # tab_result  = fetch_all_rows_(the_clickhouse_client_)
    # for row in tab_result.result_set:
    #     print(row)
