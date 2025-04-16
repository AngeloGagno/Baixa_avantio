import streamlit as st
import pandas as pd
import io
from backend.load.change_payment import execute

class App:
    def __init__(self):
        self.title()
        self.uploaded_df = None
        self.run()

    def title(self):
        st.title("Upload de Arquivo XLSX com Processamento e Envio")

    def success_message(self, message):
        st.success(message)

    def dataframe(self, file):
        return pd.read_excel(file)