from theentity.scraper.ftc_api import FTCScraper
from theentity.dbframes.event import EventScraper
import pandas as pd
from tqdm import tqdm

class MatchScraper:
    def __init__(self, username, token, minYear):
        self.scraper = FTCScraper(username, token)
        self.min_year = minYear 
        self.max_year = self.get_max_year() 
        self.event_scraper = EventScraper(username, token, minYear)

    def get_uri(self, year, event_code):
        return f"/v2.0/{year}/matches/{event_code}"

    def get_max_year(self):
        response = self.scraper.request('/v2.0')
        max_year = response.data['maxSeason']
        return max_year

    def get_matches(self, year, event_code): 
        if year < self.min_year or year > self.max_year:
            return None
        response = self.scraper.request(self.get_uri(year, event_code))
        return Match(response.data)

    def get_all_matches(self):
        matches_y = {} 
        for year in range(self.min_year, self.max_year + 1):
            events = self.event_scraper.get_events(year)
            matches = {}
            for event in tqdm(events.events):
                try:
                    matches[events.events[event][0]] = self.get_matches(year, events.events[event][0])
                except Exception as e:
                    print("Skipping event")
                    continue
            matchevent = MatchEventAccumulation(matches)
            matches_y[str(year)] = matchevent 

        return MatchYearAccumulation(matches_y)

class MatchYearAccumulation:
    def __init__(self, matches_dict):
        self.matcheevents = matches_dict

    def get_matchevent(self, year):
        return self.matcheevents[str(year)]

class MatchEventAccumulation:
    def __init__(self, matches_dict):
        self.matches = matches_dict

    def get_match(self, event):
        return self.matches[str(event)]

class Match:
    def __init__(self, match_data):
        self.data = match_data
        self.matches = {}
        for m in match_data['matches']:
            try:
                self.matches[m['matchNumber']] = [
                    m['scoreRedFinal'],
                    m['scoreRedFoul'],
                    m['scoreRedAuto'],
                    m['scoreBlueFinal'],
                    m['scoreBlueFoul'],
                    m['scoreBlueAuto'],
                    m['teams'][0]['teamNumber'],
                    m['teams'][0]['dq'],
                    [m['teams'][0]['onField']],
                    m['teams'][1]['teamNumber'],
                    m['teams'][1]['dq'],
                    [m['teams'][1]['onField']],
                    m['teams'][2]['teamNumber'],
                    m['teams'][2]['dq'],
                    [m['teams'][2]['onField']],
                    m['teams'][3]['teamNumber'],
                    m['teams'][3]['dq'],
                    [m['teams'][3]['onField']],
                ]
            except IndexError:
                print("Skipping match")
                continue

    def get_all_names(self):
        return list(self.matches.keys())

    def get_event(self, event_id):
        return self.matches[event_id]

    def get_event_count(self):
        return len(self.matches)

    def get_pandas(self):
        if len(self.matches) == 0:
            return None
        df = pd.DataFrame(self.matches).transpose()
        df = df.set_axis(['red_final', 'red_foul', 'red_auto', 'blue_final', 'blue_foul', 'blue_auto',
                          'blue1', 'blue1_dq', 'blue1_onField', 
                          'blue2', 'blue2_dq', 'blue2_onField',
                          'red1', 'red1_dq', 'red1_onField',
                          'red2', 'red2_dq', 'red2_onField'],
                         axis="columns")
        return df
