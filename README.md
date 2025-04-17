# Baixa Avantio

Sistema de atualização automatizada do status de pagamento de reservas na Avantio.

## Descrição

O Baixa Avantio é uma solução que permite atualizar o status de pagamento de reservas na plataforma Avantio de forma eficiente. O processo consiste em:

1. Usuário envia um arquivo XLSX com referências de reservas
2. Sistema verifica cada registro no banco PostgreSQL
3. Se os dados estiverem corretos, realiza um POST na API da Avantio para atualizar o status de pagamento
4. Retorna relatório com status de cada operação

## Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: 
  - SQLAlchemy (conexão com banco de dados)
  - Pandas (processamento de dados)
  - Requests (comunicação com API)
- **Infraestrutura**: Docker

## Fluxo de Funcionamento

1. O usuário faz upload do arquivo XLSX via interface Streamlit
2. O backend processa o arquivo e o armazena na pasta `archive`
3. Os dados são tratados e normalizados
4. O sistema cria uma coluna de status com três possíveis resultados:
   - **Verdadeiro**: Reserva encontrada e atualizada com sucesso
   - **Falso**: Reserva encontrada, mas com valores diferentes dos informados
   - **Não encontrado**: Reserva não localizada no banco de dados
5. Uma planilha de resultados é gerada na pasta `output` e disponibilizada para download
6. Após a conclusão, os arquivos temporários são removidos e o sistema fica pronto para nova operação

## Estrutura do Projeto

```
src/
    archive/                  # Armazenamento temporário de arquivos recebidos
    backend/ 
        database/
            query.py          # Gerenciamento de sessão e consultas no banco
        extract/
            bookings_file.py  # Extração do arquivo XLSX do frontend
        get/
            api.py            # Configuração de credenciais e corpo da requisição API
            payment_id.py     # Chamadas de função POST para atualização
        load/
            change_payment.py # Verificação e alteração de status de pagamento
            send_to_excel.py  # Processamento e envio para pasta output
        transform/
            clear_dataframe.py # Limpeza de dados, formatação de datas e colunas
        utils/
        credentials.py        # Classe de conexão com banco de dados
    frontend/
        app.py                # Interface de usuário Streamlit
    output/                   # Armazenamento dos relatórios processados
    main.py                   # Ponto de entrada da aplicação

Dockerfile
docker-compose.yml
pyproject.toml
poetry.lock
```

## Configuração e Execução

### Pré-requisitos

- Docker e Docker Compose instalados
- Credenciais de acesso ao banco de dados PostgreSQL
- API key da Avantio

### Configuração

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
host=host_do_banco
db_name=nome_da_tabela
user=seu_usuario
db_password=sua_senha
port=25060
API_AVANTIO=api_key_Avantio
```

### Execução

```bash
# Construir e iniciar containers
docker compose up --build

# Ou separadamente
docker build -t baixa_avantio .
docker compose up
```

Após a inicialização, acesse a interface web através do navegador no endereço indicado pelo Streamlit.

## Uso

1. Acesse a interface web do sistema
2. Faça upload do arquivo XLSX contendo as referências de reservas
3. Aguarde o processamento
4. Faça download do relatório gerado com os resultados das operações