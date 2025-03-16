import requests
import base64
import json

class FTCScraper:
    def __init__(self, username, token):
        self.username = username
        self.token = token
        self.myUrl = 'https://ftc-api.firstinspires.org'
        self.computed_token = base64.b64encode(bytes('{}:{}'.format(username, token), 'utf-8')).decode('utf-8')
        self.head = {'Authorization': f"Basic {self.computed_token}"}
    def request(self, uri):
        url = f"{self.myUrl}{uri}"
        response = requests.get(url, headers=self.head)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        return FTCScraperResponse(response, json.loads(response.text))


class FTCScraperResponse:
    def __init__(self, response, data):
        self.response = response
        self.data = data

    def __str__(self):
        return f"Response: {self.response}\nData: {json.dumps(self.data, indent=4)}"
