from theentity.scraper.ftc_api import FTCScraper
import json
import pandas as pd

class EventScraper:
    def __init__(self, username, token, minYear):
        self.scraper = FTCScraper(username, token)
        self.min_year = minYear 
        self.max_year = self.get_max_year() 

    def get_uri(self, year):
        return f"/v2.0/{year}/events"
    
    def get_max_year(self):
        response = self.scraper.request('/v2.0')
        max_year = response.data['maxSeason']
        return max_year

    def get_events(self, year): 
        if year < self.min_year or year > self.max_year:
            return None
        response = self.scraper.request(self.get_uri(year))
        return Event(response.data)

    def get_all_events(self):
        events = {} 
        for year in range(self.min_year, self.max_year + 1):
            events[str(year)] = self.get_events(year)
        return EventAccumulation(events)

class EventAccumulation:
    def __init__(self, events_dict):
        self.events = events_dict

    def get_event(self, year):
        return self.events[str(year)]


class Event:
    def __init__(self, event_data):
        self.data = event_data
        self.events = {}
        for s in event_data['events']:
            self.events[s['eventId']] = [s['code'], s['divisionCode'], s['name'], s['remote'], s['hybrid'], s['fieldCount'], s['published'], s['type'], s['typeName'], s['regionCode'], s['leagueCode'], s['districtCode'], s['venue'], s['address'], s['city'], s['stateprov'], s['country'], s['website'], s['liveStreamUrl'], s['coordinates'], s['webcasts'], s['timezone'], s['dateStart'], s['dateEnd']] 
        assert len(self.events) == self.data['eventCount']

    def get_all_names(self):
        return list(self.events.keys())

    def get_event(self, event_id):
        return self.events[event_id]

    def get_event_count(self):
        return len(self.events)
    
    def get_pandas(self):
        df = pd.DataFrame(self.events).transpose()
        df = df.set_axis(['code', 'divisionCode', 'name', 'remote', 'hybrid', 'fieldCount', 'published', 'type', 'typeName', 'regionCode', 'leagueCode', 'districtCode', 'venue', 'address', 'city', 'stateprov', 'country', 'website', 'liveStreamUrl', 'coordinates', 'webcasts', 'timezone', 'dateStart', 'dateEnd'], axis="columns") 
        return df
