import os
import pandas as pd
from pathlib import Path

class Excel:
    def __init__(self):
        self.download_path = self.download_folder()
        self.dataframe = self.get_excel()
    def download_folder(self):
        download = Path.home() / 'Downloads'
        return download

    def get_excel(self):
        path = self.download_path
        
        return pd.read_excel(path / 'teste2.xlsx')
        
    def __repr__(self):
        return repr(self.dataframe)  

if __name__ == '__main__':
    print(Excel())