
from backend.load.change_payment import execute

def send_to_excel():
    df = execute()
    df.to_excel('output/Arquivo.xlsx',index=None)