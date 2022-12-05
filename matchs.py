import json
from datetime import date

with open('matchs.json', 'r') as f:
    data = json.load(f)

today = [match for match in data['matchs'] if match['date'] == str(date.today())]