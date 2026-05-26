import clickhouse_connect
from db_utils_.establish_connection_clickhouse_ import get_clickhouse_client_
import db_utils_.db_commands_ as db_commands_
import tomllib
from pathlib import Path

def clickhouse_client_():
    """
    Wrapper function to establish and return a ClickHouse client connection.
    """
    a_clickhouse_client_ = get_clickhouse_client_()
    return a_clickhouse_client_

def fetch_all_rows_(a_client_):
    """
    Reads the target table name from pyproject.toml, fetches all rows 
    from ClickHouse as a DataFrame, and returns the result.
    
    Args:
        a_client_: The active ClickHouse client instance.
    Returns:
        pd.DataFrame: The queried data.
    """
    # Build path to config relative to the project root
    parent_dir = Path(__file__).resolve().parent.parent
    config_path = str(parent_dir / "pyproject.toml").replace("\\", "/")
    
    # Load table configuration
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    
    tab_name_ = data["clickhouse-db"]["table_name_"]
    
    # Generate query via utility function and execute
    fetch_data_query_ = db_commands_.fetch_all_entries_from_table(table_name_=tab_name_)
    tab_result = a_client_.query_df(fetch_data_query_)
    
    print('Tab Result Set --- >>> ', tab_result)
    return tab_result

if __name__ == "__main__":
    # Initialize connection and fetch data
    the_clickhouse_client_ = clickhouse_client_()  
    tab_result = fetch_all_rows_(the_clickhouse_client_)
    
    # Iterate through DataFrame (assuming standard pandas access)
    # Note: query_df returns a DataFrame, so we iterate rows if required
    for index, row in tab_result.iterrows():
        print(row)