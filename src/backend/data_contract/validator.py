import pandas as pd
from backend.data_contract.model import Datamodel

def validate_dataframe_with_pydantic(df: pd.DataFrame):
    errors = []
    validated_rows = []

    df = df.rename(columns={"Data de pagamento": "Data_de_pagamento"})

    for index, row in df.iterrows():
        try:
            item = Datamodel(**row.to_dict())
            validated_rows.append(item)
        except Exception as e:
            errors.append(f"Linha {index + 1}: {e}")

    if errors:
        return False, errors, None
    else:
        validated_df = pd.DataFrame([item.dict() for item in validated_rows])
        validated_df = validated_df.rename(columns={"Data_de_pagamento": "Data de pagamento"})
        return True, None, validated_df
