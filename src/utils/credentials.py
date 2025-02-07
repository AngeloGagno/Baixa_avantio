from dotenv import load_dotenv 
import os

class DBConfig:
    @staticmethod
    def get_env_config():
        load_dotenv(override=True)
        return {
            "host": os.getenv('host'),
            "database": os.getenv('db_name'),
            "user": os.getenv('user'),
            "password": os.getenv('db_password'),
            "port": os.getenv('port'),
        }
