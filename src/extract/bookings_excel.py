import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
class Excel:
    def __init__(self):
        self.download_path = self.download_folder()
        self.dataframe = self.get_excel()
    def download_folder(self):
        download = Path.home() / 'Downloads'
        return download

    def get_excel(self):
        load_dotenv(override=True)
        path = self.download_path
        
        return pd.read_excel(path / os.getenv('Archive_name') )
        
    def __repr__(self):
        return repr(self.dataframe)  

if __name__ == '__main__':
    print(Excel())