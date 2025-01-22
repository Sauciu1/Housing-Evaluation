import unittest
from datetime import datetime
from Navigator import Navigator
import json

class TestTravelTime(unittest.TestCase):
    def test_set_time_day(self):
        expected_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        actual_time = Navigator._set_time("day")
        self.assertEqual(actual_time.hour, expected_time.hour)
        self.assertEqual(actual_time.minute, expected_time.minute)

    def test_set_time_night(self):
        expected_time = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)
        actual_time = Navigator._set_time("night")
        self.assertEqual(actual_time.hour, expected_time.hour)
        self.assertEqual(actual_time.minute, expected_time.minute)

    def test_set_time_now(self):
        actual_time = Navigator._set_time("now")
        self.assertEqual(actual_time, datetime.now())

    def test_set_time_invalid(self):
        with self.assertRaises(ValueError):
            Navigator._set_time("invalid")



class TestInsertToDB(unittest.TestCase):
    def setUp(self):
        self.navigator = Navigator()

    def test_insert_to_db(self):
        results = {
            "duration": 30,
            "distance": 10.5,
            "origin": "Origin",
            "destination": "Destination",
            "time_of_day": "day",
            "mode": "transit",
            "directions": [{"legs": [{"duration": {"text": "30 mins"}, "distance": {"text": "10.5 km"}}]}]
        }
        self.navigator._insert_to_db(results)
        self.navigator._insert_to_db(results)



if __name__ == "__main__":
    unittest.main()