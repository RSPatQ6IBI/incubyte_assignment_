import clickhouse_connect
import os
from dotenv import load_dotenv
from pathlib import Path

def fetch_env_keys_():
    load_dotenv()
    # host_ = os.getenv('CLICKHOUSE_HOST_NAME_')
    user_ = os.getenv('CLICKHOUSE_USER_NAME_')
    password_ = os.getenv('CLICKHOUSE_USER_PASSWORD_')
    import tomllib
    parent_dir = Path(__file__).resolve().parent.parent
    config_path = str(parent_dir / "pyproject.toml")
    config_path = config_path.replace("\\", "/")

    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    host_ = data["clickhouse-db"]["clickhouse_host_name_"]   # Nested entries (tables)
    return host_, user_, password_


def get_clickhouse_client_():
    host_, user_, password_ = fetch_env_keys_()
    
    client = clickhouse_connect.get_client(
        host = host_,
        user= user_,
        password = password_,
        secure=True
    )
    return client

# FUNCTION USAGE
# if __name__ == "__main__":
#     clickhouse_client_ = get_clickhouse_client_()
#     print(clickhouse_client_)
