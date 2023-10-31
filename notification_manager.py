import requests, os
from twilio.rest import Client
import smtplib
from datetime import datetime
from data_manager import DataManager

my_email = "testingthsbtch@gmail.com"
password = "gsxvjtawvosuvybs"
phone_number = os.environ.get("PHONE_NUMBER")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
BITLY_ACCESS_TOKEN = os.environ.get("BITLY_ACCESS_TOKEN")
class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)
        self.data_manager = DataManager()
        self.users_data = self.data_manager.get_users_email()

    def shorten_url(self, long_url):
        headers = {
            "Authorization": f"Bearer {BITLY_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "long_url": long_url
        }
        response = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, json=data)
        shortened_url = response.json().get("link", "")
        return shortened_url
    def send_message(self, price, departure_city, departure_iata, arrival_city, arrival_city_iata,outbound_date,
                     inbound_date, link, extra_info=""):
        shortened_link = self.shorten_url(link)
        body = f"Low price alert! Only ${price} to fly from {departure_city}-{departure_iata} to" \
               f" {arrival_city}-{arrival_city_iata},from {outbound_date} to {inbound_date}\n{link}\n" \
               f"{extra_info}"

        message = self.client.messages.create(
            body=body,
            from_=phone_number,
            to='+1 239 821 6857'
        )
        # print(message.status)

    def send_email(self, price, departure_city, departure_iata, arrival_city, arrival_city_iata,outbound_date,
                     inbound_date, link, extra_info=""):
        for user in self.users_data:
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()  # makes connection secure
                    connection.login(user=my_email, password=password)
                    subject = f"Subject: Low price alert! {departure_city} to {arrival_city} - {datetime.now()}"
                    connection.sendmail(from_addr=my_email,
                                        to_addrs=f"{user['email']}",
                                        msg=f"Subject: {subject}\n\n Only ${price} to fly from {departure_city}-{departure_iata} to" \
                       f" {arrival_city}-{arrival_city_iata},from {outbound_date} to {inbound_date}" \
                       f"{extra_info}")
                    connection.close()
            except IndexError:
                print("No data in the emails column!")
            




