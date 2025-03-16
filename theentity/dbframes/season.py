from theentity.scraper.ftc_api import FTCScraper
import pandas as pd

class SeasonScraper:
    def __init__(self, username, token, minYear):
        self.scraper = FTCScraper(username, token)
        self.min_year = minYear 
        self.max_year = self.get_max_year() 

    def get_uri(self, year):
        return f"/v2.0/{year}"
    
    def get_max_year(self):
        response = self.scraper.request('/v2.0')
        max_year = response.data['maxSeason']
        return max_year

    def get_season(self, year): 
        if year < self.min_year or year > self.max_year:
            return None
        response = self.scraper.request(self.get_uri(year))
        return Season(response.data)

    def get_all_seasons(self):
        seasons = {} 
        for year in range(self.min_year, self.max_year + 1):
            seasons[str(year)] = self.get_season(year)
        return SeasonAccumulation(seasons)

class SeasonAccumulation:
    def __init__(self, seasons_dict):
        self.seasons = seasons_dict

    def get_season(self, year):
        return self.seasons[str(year)]


class Season:
    def __init__(self, season_data):
        self.data = season_data
        self.gameName = season_data['gameName']
        self.rookieStart = season_data['rookieStart']
        self.teamCount = season_data['teamCount']
        self.seasonMatches = {}
        for s in season_data['fRCChampionships']:
            self.seasonMatches[s['name']] = [s['startDate'], s['location']]

    def get_all_names(self):
        return list(self.seasonMatches.keys())

    def get_championship(self, name):
        return self.seasonMatches[name]

    def get_event_count(self):
        return len(self.seasonMatches)
    
    def get_pandas(self):
        df = pd.DataFrame(self.seasonMatches).transpose()
        df = df.set_axis(['startDate', 'location'], axis='columns')
        return df
