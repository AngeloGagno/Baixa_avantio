import streamlit as st
import pandas as pd
import io
from backend.load.change_payment import execute
from backend.data_contract.validator import validate_dataframe_with_pydantic

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

    def upload_button(self, types: list = ["xlsx"]):
        uploaded_file = st.file_uploader("Faça upload do seu arquivo .xlsx", type=types)

        if uploaded_file is not None:
            try:
                df = self.dataframe(uploaded_file)
                self.success_message("Arquivo carregado com sucesso!")
                st.dataframe(df)
                validation_passed, errors, validated_df = validate_dataframe_with_pydantic(df)

                if validation_passed:
                    st.success("Dataframe validado com sucesso!")
                    return validated_df
                else:
                    st.error("Falha na validação, verifique o nome das colunas ou se o formato está correto. "
                    "Favor verificar e enviar novamente.")
                    return None

            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")
                return None
        else:
            st.info("Aguardando o upload do arquivo.")
            return None

    def send_button(self):
        if st.button("Clique para começar a dar baixa"):
            if self.uploaded_df is not None:
                with st.spinner("Processando os dados..."):

                    resultado_df = execute()
                    st.success("Baixa concluída!")
                    st.dataframe(resultado_df)

                    # Gera um arquivo Excel para download
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        resultado_df.to_excel(writer, index=False, sheet_name='Resultado')
                    output.seek(0)

                    st.download_button(
                        label="Clique para Baixar o resultado",
                        data=output,
                        file_name="resultado_processado.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning("Nenhum dado para enviar. Faça o upload primeiro!")

    def run(self):
        self.uploaded_df = self.upload_button()

        if self.uploaded_df is not None:
            self.send_button()