
from pathlib import Path
import tomllib
import pandas as pd

def get_emp_details_from_raw_txt_():
    parent_dir = Path(__file__).resolve().parent.parent
    config_path = str(parent_dir / "pyproject.toml")
    config_path = config_path.replace("\\", "/")
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
        data_dir_  = data["clickhouse-db"]["local_dir_data_"]
        file_emp_first_names_ = data["clickhouse-db"]["employee_first_name_list_"]
        file_emp_last_names_ = data["clickhouse-db"]["employee_last_name_list_"]
        file_emp_gross_sal_ = data["clickhouse-db"]["employee_gross_salary_list_"]
        file_emp_locs_ = data["clickhouse-db"]["employee_location_list_"]
        file_emp_timezones_ = data["clickhouse-db"]["employee_timezone_list_"]
        emp_first_names_ = pd.read_csv(data_dir_+file_emp_first_names_,  names=['first_names'])
        emp_last_names_ = pd.read_csv(data_dir_+file_emp_last_names_,  names=['last_names'])
        emp_gross_sal_ = pd.read_csv(data_dir_+file_emp_gross_sal_,  names=['gross_sal'])
        emp_locs_ = pd.read_csv(data_dir_+file_emp_locs_,  names=['emp_locs'])
        emp_timezones_ = pd.read_csv(data_dir_+file_emp_timezones_,  names=['emp_timezone_'])
        if emp_first_names_.empty or emp_last_names_.empty or emp_gross_sal_.empty or emp_timezones_.empty:
            print("Check the raw data files, these may be empty -- >>> ") 
            exit
        else:
            return emp_first_names_, emp_last_names_, emp_gross_sal_, emp_locs_, emp_timezones_


##### TEST FUNCTION USAGE
if __name__ == "__main__":
    emp_first_names_, emp_last_names_, emp_gross_sal_, emp_locs_, emp_timezones_ = get_emp_details_from_raw_txt_()
    print(emp_first_names_.head())
    print(emp_gross_sal_.head())
    print(emp_locs_.head())
    print(emp_timezones_.head())
    
    
    