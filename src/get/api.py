import requests
import os 
from dotenv import load_dotenv


class API_Request:
    def __init__(self, id, request_type):
        self.request_type = request_type
        self.api_key = self._API_Key()
        self.id = id
        self.url = self._url()
        self.header = self._headers()
        

    def _API_Key(self):
        load_dotenv(override=True)
        return os.getenv('API_AVANTIO')

    def _url(self):
        return f'https://api.avantio.pro/pms/v2/bookings/{self.id}'

    def _headers(self):
        if self.request_type == 'put':
            return {
                "accept": "application/json",
                "content-type": "application/json",
                "X-Avantio-Auth": self.api_key
            }
        elif self.request_type == 'get':
            return {"accept": "application/json",
            "X-Avantio-Auth": self.api_key}
        else:
            raise TypeError("Invalid request type. Use 'get' or 'put'.")

    def bookings_id(self):
        return requests.get(self.url, headers=self.header)

    def verify_status(self):
        return self.bookings_id().status_code

    def get_bookings(self):
        if self.verify_status() == 200:
            return self.bookings_id().json()
        return None

    def _update_payment(self, payment_id, paid_date):
        return {
            "payments": [
                {
                    "id": payment_id,
                    "status": "PAID",
                    "paymentMethod": "BANK_TRANSFER",
                    "paidDate": paid_date
                }
            ]
        }

    def set_update(self, payment_id, paid_date):

        payload = self._update_payment(payment_id, paid_date)
        response = requests.put(self.url, json=payload, headers=self.header)

        if response.status_code == 200:
            print(response)
        else:
            return {"error": f"Failed to update payment. Status code: {response.status_code}"}