import streamlit as st
from backend.extract.bookings_file import Excel
from backend.load.send_to_excel import send_to_excel
from pathlib import Path
import os
import uuid

class App:
    def __init__(self):     
        self.input_path = Path(__file__).parents[1] / 'archive'
        self.output_path = Path(__file__).parents[1] / 'output'
        
        # Criar diretórios se não existirem
        self.input_path.mkdir(exist_ok=True)
        self.output_path.mkdir(exist_ok=True)
        
        # Limpar pasta archive no início da sessão
        self.clean_archive_folder()
        
        # Nome do arquivo de saída
        self.output_file_name = "Arquivo.xlsx"
        self.uploaded_file_path = None
        
        # Inicializar estado da sessão
        if 'processed' not in st.session_state:
            st.session_state.processed = False
        if 'downloaded' not in st.session_state:
            st.session_state.downloaded = False
        if 'uploader_id' not in st.session_state:
            st.session_state.uploader_id = str(uuid.uuid4())
    
    def clean_archive_folder(self):
        """Limpa todos os arquivos da pasta archive"""
        for file in self.input_path.glob('*'):
            if file.is_file():
                os.remove(file)
    
    def title(self):
        st.title("Sistema de Baixa na AVANTIO")
    
    def reset_app_state(self):
        """Redefine o estado do aplicativo e gera um novo ID para o uploader"""
        self.clean_archive_folder()
        self.clean_output_file()
        st.session_state.processed = False
        st.session_state.downloaded = False
        st.session_state.uploader_id = str(uuid.uuid4())  # Gera um novo ID para forçar um novo uploader
        st.rerun()
    
    def upload_box(self):
        # Usar um ID dinâmico para o uploader baseado no estado da sessão
        uploaded_file = st.file_uploader(
            label='Adicione o arquivo XLSX para dar baixa', 
            type=['xlsx'],
            accept_multiple_files=False,
            key=f"file_uploader_{st.session_state.uploader_id}"
        )
        
        if uploaded_file:
            # Salvar o arquivo carregado
            file_path = self.input_path / uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.read())
            self.uploaded_file_path = file_path
            return True
        return False
    
    def button_verify(self):
        return st.button('Clique para executar', disabled=st.session_state.processed)
    
    def clean_output_file(self):
        """Remove o arquivo de saída"""
        output_file = self.output_path / self.output_file_name
        if output_file.exists():
            os.remove(output_file)
    
    def download_button(self):
        output_file = self.output_path / self.output_file_name
        
        if output_file.exists():
            col1, col2 = st.columns([3, 1])
            
            with open(output_file, "rb") as file:
                file_data = file.read()
                
            with col1:
                download_clicked = st.download_button(
                    label='Arquivo Finalizado, clique para fazer o download',
                    data=file_data,
                    file_name=self.output_file_name,
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            
            with col2:
                if st.button("Reiniciar"):
                    self.reset_app_state()
                    
            return download_clicked
        return False
    
    def run(self):
        self.title()
        
        # Upload do arquivo
        file_uploaded = self.upload_box()
        
        # Botão para processar
        if file_uploaded and not st.session_state.processed:
            button = self.button_verify()
            
            if button and self.uploaded_file_path:
                try:
                    # Processar o arquivo
                    send_to_excel()
                    
                    # Marcar como processado
                    st.session_state.processed = True
                    
                    # Mostrar mensagem de sucesso
                    st.success('Arquivo processado com sucesso!')
                    
                    # Rerun para atualizar a interface
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Verifique o arquivo e se as colunas estão em conformidade.")
                    if self.uploaded_file_path and self.uploaded_file_path.exists():
                        os.remove(self.uploaded_file_path)
        
        # Mostrar botão de download se o arquivo foi processado
        if st.session_state.processed:
            self.download_button()
