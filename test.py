from theentity.dbframes.matches import MatchScraper 
import pandas

username = 'jackolantern'
token = "65DE823D-2B7D-4265-8E87-FE9C1036107F"

scraper = MatchScraper(username, token, 2015)

a = scraper.get_all_matches()
all_events = []
all_data = []
for year in range(2015, 2024+1):
    events = a.get_matchevent(year).matches.keys()

    for event in events:
        all_data.append(a.get_matchevent(year).matches[event].get_pandas())



df = pandas.concat(all_data, axis=0)

print(df)
df.to_csv('DATA.csv', index=True)
