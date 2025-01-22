import googlemaps
import duckdb as ddb
from datetime import datetime 
import json
from get_key import get_key

class Navigator:
    def __init__(self, api_key= None):
        self.api_key = get_key() if api_key is None else api_key
        self.g_maps = googlemaps.Client(key=self.api_key)
        self.ddb_con = ddb.connect('travel_data.db')


    @staticmethod
    def _set_time(time_of_day="day"):
        """Allows to account for day and night Public Transport differing"""
        if time_of_day == "day":
            departure_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        elif time_of_day == "night":
            departure_time = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)
        elif time_of_day == "now":
            departure_time = datetime.now()
        else:
            raise ValueError("Invalid option chosen")
        return departure_time

    def _directions_call(self, origin: str, destination: str, mode: str, time_of_day: str):
        """Make the call to gmaps api and process the result"""
        directions = self.g_maps.directions(
            origin,
            destination,
            mode=mode,
            departure_time=self._set_time(time_of_day))

        if directions:
            duration = int(directions[0]['legs'][0]['duration']['text'].replace("mins", ""))
            distance = float(directions[0]['legs'][0]['distance']['text'].replace("km", ""))
            return {
                "duration": duration,
                "distance": distance,
                "origin": origin,
                "destination": destination,
                "mode": mode,
                "time_of_day": time_of_day,
                "directions": directions
            }
        else:
            raise AssertionError("No directions response")
        

    def _insert_to_db(self, results):
        """Insert new DB row"""
        result = self.ddb_con.execute('''
        INSERT INTO travel_info (duration, distance, origin, destination, mode, time_of_day, directions) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (results['duration'], results['distance'], results['origin'], results['destination'], results['mode'], results['time_of_day'], json.dumps(results['directions'])))

        if result.rowcount == 0:
            raise AssertionError("Insert to database failed")
        self.ddb_con.commit()


    def _get_unique_directions(self, origin, destination, mode="transit", time_of_day="day"):
        """"""
        results =  self._directions_call(origin, destination, mode, time_of_day)
        results["departure_time"] =time_of_day
        self._insert_to_db(results)
        return results
    


        

    def get_directions(self, origin, destination, mode="transit", time_of_day="day"):
        """Choose whether information exists or needs to be called"""

        query = '''
        SELECT * FROM travel_info 
        WHERE origin = ? AND destination = ? AND mode = ? AND time_of_day = ?
        '''
        existing_entry = self.ddb_con.execute(query, (origin, destination, mode, time_of_day)).fetchone()
        
        if existing_entry:
            existing_entry = {
            "duration": existing_entry[0],
            "distance": existing_entry[1],
            "origin": existing_entry[2],
            "destination": existing_entry[3],
            "mode": existing_entry[4],
            "time_of_day": existing_entry[5],
            "directions": json.loads(existing_entry[6])
            }

        if existing_entry:
            return existing_entry
        else:
            return self._get_unique_directions(origin, destination, mode, time_of_day)


if __name__ == "__main__":


    navigator = Navigator()

    origin = "West Kensington, London"
    destination = "SW13 9BN"
    travel = navigator.get_directions(origin, destination)
    print(travel['duration'], travel['distance'], travel['time_of_day'])
