from pydantic import BaseModel
from datetime import datetime

class Datamodel(BaseModel):
    Data_de_pagamento: datetime
    Descrição: str 
    Valor: float