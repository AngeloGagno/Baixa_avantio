from sqlalchemy import create_engine, text

class Connection_DB:
    def __init__(self,host,database,user,password,port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = self._connection_string()
        self.engine = self._creating_engine()
        self.close = self.close_connection()
    def _connection_string(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def _creating_engine(self):
        return create_engine(self.connection)

    def close_connection(self):
        if self.engine:
            self.engine.dispose()

    def query(self, db_query):
        query = text(db_query)

        with self.engine.connect() as conn:
            result = conn.execute(query)
            row = result.fetchone()  # Pega a primeira linha
            self.close
        return (row[0], row[1]) if row else (None, None)