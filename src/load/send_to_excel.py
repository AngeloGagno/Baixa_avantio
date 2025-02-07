import pandas as pd
from load.change_payment import execute

def send_to_excel():
    df = execute()
    df.to_excel('Teste.xlsx',index=None)