from get.api import API_Request

def get_payment_id(id):
    return API_Request(id,'get').get_bookings()['data']['payments'][0]['id']

def change_payment_configs(id,paid_date):
    payment_id = get_payment_id(id)
    API_Request(id,'put').set_update(payment_id,paid_date=paid_date)