import pandas as pd
from Navigator import Navigator

class Person():
    """Stores locations of interest for each individual"""
    def __init__(self, navigator, origin, name = None):
        self.navigator = navigator
        self.name = name
        self.destinations = {}
        self.mode = {"transit": 1, "walking": 1}
        self.time = {"day": 1, "night":1} 
        self.origin = origin

    def _normalize_dict(self, importance:dict):
        """makes sure that a dictionary sums to 1. Removes non-important"""
        total = sum(importance.values())
        if total > 0:
            importance = {k: v / total for k, v in importance.items()}
        importance = {k: v for k, v in importance.items() if v != 0}
        return importance

    def go_there(self):
        """Iterates through all conditions and returns them as pandas dataframe"""
        self.destinations = self._normalize_dict(self.destinations)
        self.mode = self._normalize_dict(self.mode)
        self.time = self._normalize_dict(self.time)

        self.results =pd.DataFrame()
        for location, loc_importance in self.destinations.items():
            for mode, mode_importance in self.mode.items():
                for time, time_importance in self.time.items():
                    directions = self.navigator.get_directions(self.origin, location, mode, time)
                    
                    del directions['directions']
                    
                    directions['location_importance'] = loc_importance
                    directions['mode_importance'] = mode_importance
                    directions['time_importance'] = time_importance
                    directions['name'] = self.name
                    
                    self.results = pd.concat([self.results, pd.DataFrame([directions])], ignore_index=True)

        
if __name__ == "__main__":
    Povilas = Person( Navigator(), "SW13 9BN", "Povilas")
    Povilas.destinations = {"Imperial College London, South Kensington Campus":1,
                        "Imperial College London, White City Campus":1}


    Povilas.go_there()
    print(Povilas.results)