import json
import requests
from app import app
from bleach.sanitizer import Cleaner
import os


ELECTION_URL = "https://www.googleapis.com/civicinfo/v2/elections"
VOTERINFO_URL = "https://www.googleapis.com/civicinfo/v2/voterinfo"

cleaner = Cleaner()  # for use with user address info


def get_elections():
    raw_data = requests.request('GET', ELECTION_URL,
            params={'key': app.config['GOOGLE_CIVIC_KEY']})  # noqa
    data = json.loads(raw_data.content.decode('utf-8-sig'))
    elections = [e for e in data['elections'] if e['id'] not in '2000']
    return elections


def get_election_names():
    raw_data = requests.request('GET', ELECTION_URL,
            params={'key': app.config['GOOGLE_CIVIC_KEY']})  # noqa
    data = json.loads(raw_data.content.decode('utf-8-sig'))
#     elections = [e for e in data['elections'] if e['id'] not in '2000']
    elections = [e for e in data['elections']]  # for testing
    return [(e['id'], e['name']) for e in elections]


def get_polling_addresses(address, electionId):

    raw_data = requests.request('GET', VOTERINFO_URL,
            params={'key': app.config['GOOGLE_CIVIC_KEY'],  # noqa
                    'address': cleaner.clean(address),
                    'electionId': str(int(electionId))})
    data = json.loads(raw_data.content.decode('utf-8-sig'))
    return data
