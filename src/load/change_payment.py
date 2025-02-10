from transform.clear_dataframe import transform_dataframe,queries,transform_df_date,finish_date_clear
from get.payment_id import change_payment_configs

def execute():
    try:
        excel = transform_dataframe()
        for line in range(0,len(excel)):
            descricao = excel['Descrição'][line]
            payment_date = excel['Data de pagamento'][line]
            valor,booking_id = queries(query = f"select (total_payment - portal_comission) as valor, id_booking from bookings where portal_reference like '%{descricao}%'")
            print(excel.iloc[line])
            if valor == None:
                  excel.loc[line,'Status'] = 'Nao encontrado'

            elif int(valor) == int(excel['Valor'][line]):
                excel.loc[line,'Status'] = 'Verdadeiro'
                    
                change_payment_configs(id = booking_id,paid_date=payment_date)
    except Exception as e:
                print(e)
                return excel
    
    excel = finish_date_clear(excel)
    return excel

