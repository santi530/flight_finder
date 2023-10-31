from data_manager import DataManager
from flight_search import FlightSearch

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch(sheet_data)
for city in sheet_data:
    if city["iataCode"] == '':
        city["iataCode"] = flight_search.get_destination_code(city["city"])

data_manager.update_destination_code()
data_manager.destination_data = sheet_data





