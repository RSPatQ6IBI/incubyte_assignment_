import db_utils_.prepare_data_for_table_ as import_data
from db_utils_.establish_connection_clickhouse_ import get_clickhouse_client_
# import prepare_data_for_table_ as import_data
# from establish_connection_clickhouse_ import get_clickhouse_client_
import clickhouse_connect
from pathlib import Path
import db_utils_.db_commands_ as db_commands_
# import db_commands_ as db_commands_
import pandas as pd

def check_or_create_table_():
    clickhouse_client_ = get_clickhouse_client_()

    import tomllib
    parent_dir = Path(__file__).resolve().parent.parent
    config_path = str(parent_dir / "pyproject.toml")
    config_path = config_path.replace("\\", "/")
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    table_ = data["clickhouse-db"]["table_name_"]   # Nested entries (tables)
    table_cols_ = data["clickhouse-db"]["table_columns_"]   # Nested entries (tables)
    
    check_table_ = clickhouse_client_.command(db_commands_.check_table(table_name_=table_))

    if check_table_==0:
        print("creating the table -- > ")
        create_table_ = clickhouse_client_.command(db_commands_.command_create_find_table(table_name_=table_))
        check_table_ = clickhouse_client_.command(db_commands_.check_table(table_name_=table_))
        print("Table created -- >> ", check_table_)
    else:
        print('Table already exists -- >>')
    return clickhouse_client_, table_, table_cols_

def prep_data_to_insert_():
    emp_first_names_, emp_last_names_, emp_gross_sal_, emp_locs_, emp_timezones_ = import_data.get_emp_details_from_raw_txt_()
    emp_locs_.index = range(0,10000)
    mgrd_ = pd.concat([emp_first_names_, emp_last_names_], axis=1)
    mgrd_ = pd.concat([mgrd_, emp_gross_sal_], axis=1)
    mgrd_ = pd.concat([mgrd_, emp_locs_], axis=1)
    mgrd_ = pd.concat([mgrd_, emp_timezones_], axis=1)
    return mgrd_

def insert_dataframes_to_table_(the_client_, this_table_, the_tab_cols_, the_mgrd_data_):
    emp_first_names_, emp_last_names_, emp_gross_sal_, emp_locs_, emp_timezones_ = import_data.get_emp_details_from_raw_txt_()
    print('Making the table blank .. ')
    the_client_.command(db_commands_.delete_all_entries_from_table(table_name_=this_table_))
    the_client_.insert(this_table_, the_mgrd_data_, column_names=the_tab_cols_)
    print("Inserted entries from txt  .. ")


#### FUNCTION USAGE
if __name__ == "__main__":
    this_client_, the_table_, the_table_cols_ = check_or_create_table_()
    data_from_txt_ = prep_data_to_insert_()
    insert_dataframes_to_table_(this_client_, the_table_, the_table_cols_, data_from_txt_)
    
    