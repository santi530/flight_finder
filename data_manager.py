import requests

SHEET_GET_ENDPOINT_USERS = "https://api.sheety.co/06f17cab647e13601e0c47373a30a364/flightDeals/users"
SHEET_GET_ENDPOINT_PRICES = "https://api.sheety.co/06f17cab647e13601e0c47373a30a364/flightDeals/prices"
SHEETY_PASSWORD = "Basic c2FudGlhZ29fYWx2YXJlejAyOkJhcmNlbG9uYTIwMjA="

class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.header = {"Authorization": SHEETY_PASSWORD}


    def get_destination_data(self):
        response = requests.get(url=SHEET_GET_ENDPOINT_PRICES, headers=self.header)
        # print(response.text)
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEET_GET_ENDPOINT_PRICES}/{city['id']}",
                json=new_data,
                headers=self.header
            )
            # print(response.text)
    def get_users_email(self):
        response = requests.get(
            url=SHEET_GET_ENDPOINT_USERS,
            headers=self.header
        )
        users = response.json()["users"]
        return users

