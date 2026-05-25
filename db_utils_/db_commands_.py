
def command_create_find_table(table_name_):
    return f'''CREATE TABLE default.{table_name_} (
    `First_Name` String DEFAULT 'Mark',
    `Last_Name` String DEFAULT 'Braun',
    `Gross_Salary` Int64 DEFAULT '20000',
    `Employee_Location` String DEFAULT 'New Delhi',
    `Time_Zone` String DEFAULT 'GMT/BST (UTC+0 / UTC+1)'
)
'''


def check_table(table_name_):
    return f'''EXISTS TABLE default.{table_name_}'''


def delete_all_entries_from_table(table_name_):
    return f'''TRUNCATE TABLE default.{table_name_}'''

def fetch_all_entries_from_table(table_name_):
    return f'''SELECT * FROM default.{table_name_}'''

def delete_selected_entries_from_table(table_name_, first_name_val_, last_name_val_, sal_val_):
    return f'''DELETE FROM default.{table_name_} WHERE First_Name = {first_name_val_} AND Last_Name = {last_name_val_} AND Gross_Salary = {sal_val_} '''

