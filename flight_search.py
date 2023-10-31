import requests,os, pprint
from datetime import datetime, timedelta
from flight_data import FlightData
from notification_manager import NotificationManager
TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"

ORIGIN_CITY_IATA = "MIA"

class FlightSearch:

    def __init__(self, sheet_data):
        self.headers = {"apikey": TEQUILA_API_KEY}
        self.departure_date = (datetime.now() + timedelta(days=1))
        self.six_months_from_today = timedelta(days=180)
        self.to_date = (self.six_months_from_today + self.departure_date)
        self.notification_manager = NotificationManager()
        for destination in sheet_data:
            flight_data = self.search_flight(fly_to=destination["iataCode"])

            if flight_data == None:
                continue # skips to next destination

            if destination["lowestPrice"] > flight_data.price:
                if flight_data.stop_overs > 0:
                    self.notification_manager.send_message(flight_data.price, flight_data.origin_city,
                                                           flight_data.origin_airport, flight_data.destination_city,
                                                           flight_data.destination_airport, flight_data.out_date,
                                                           flight_data.return_date, flight_data.link,
                                                           extra_info=f"\nFlight has {flight_data.stop_overs} "
                                                                      f"stop over, via {flight_data.via_city}.")
                    self.notification_manager.send_email(flight_data.price, flight_data.origin_city,
                                                           flight_data.origin_airport, flight_data.destination_city,
                                                           flight_data.destination_airport, flight_data.out_date,
                                                           flight_data.return_date, flight_data.link,
                                                           extra_info=f"\nFlight has {flight_data.stop_overs} "
                                                                      f"stop over, via {flight_data.via_city}.")
                else:
                    self.notification_manager.send_message(flight_data.price, flight_data.origin_city,
                                                           flight_data.origin_airport, flight_data.destination_city,
                                                           flight_data.destination_airport, flight_data.out_date,
                                                           flight_data.return_date, flight_data.link)
                    self.notification_manager.send_email(flight_data.price, flight_data.origin_city,
                                                           flight_data.origin_airport, flight_data.destination_city,
                                                           flight_data.destination_airport, flight_data.out_date,
                                                           flight_data.return_date, flight_data.link)

    def get_destination_code(self, city_name):
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/locations/query",
            params=query,
            headers=self.headers
        )
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def search_flight(self, fly_to):
        flight_search_query = {
                "fly_from": ORIGIN_CITY_IATA,
                "fly_to": fly_to,
                "date_from": self.departure_date.strftime("%d/%m/%Y"),
                "date_to": self.to_date.strftime("%d/%m/%Y"),
                "curr": "USD",
                "locale": "en",
                "max_stopovers": 0,
                "vehicle_type": "aircraft",
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "one_for_city": 1,
            }
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            params=flight_search_query,
            headers=self.headers
        )
        try:
            search_data = response.json()["data"][0]
            # pprint.pprint(search_data)
            # print(f"Price found for {fly_to}: ${search_data['price']}")

        except IndexError:
            flight_search_query["max_stopovers"] = 2
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=self.headers,
                params=flight_search_query,
            )
            search_data = response.json()["data"][0]
            # pprint.pprint(search_data)
            flight_data = FlightData(
                price=search_data["price"],
                origin_city=search_data["route"][0]["cityFrom"],
                origin_airport=search_data["route"][0]["flyFrom"],
                destination_city=search_data["route"][1]["cityTo"],
                destination_airport=search_data["route"][1]["flyTo"],
                out_date=search_data["route"][0]["local_departure"].split("T")[0],
                return_date=search_data["route"][2]["local_departure"].split("T")[0],
                link=search_data["deep_link"],
                stop_overs=1,
                via_city=search_data["route"][0]["cityTo"]
            )
            return flight_data

        else:
            flight_data = FlightData(
                price=search_data["price"],
                origin_city=search_data["route"][0]["cityFrom"],
                origin_airport=search_data["route"][0]["flyFrom"],
                destination_city=search_data["route"][0]["cityTo"],
                destination_airport=search_data["route"][0]["flyTo"],
                out_date=search_data["route"][0]["local_departure"].split("T")[0],
                return_date=search_data["route"][1]["local_departure"].split("T")[0],
                link=search_data["deep_link"]
            )
            return flight_data








