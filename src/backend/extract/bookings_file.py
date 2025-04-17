import pandas as pd
from pathlib import Path

class Excel:
    def __init__(self):
        self.folder = self.download_folder()
        self.file_name = self.get_files()      

    def download_folder(self):
        folder = Path(__file__).parents[2] / 'archive'
        return folder

    def get_files(self):
        for archive in self.folder.glob('*.xlsx'):
            return archive

        else: 
            raise FileNotFoundError('Arquivo Não encontrado.')

    def read_file(self):
        return pd.read_excel(self.file_name)
    
    def delete_file(self):
        self.file_name.unlink()