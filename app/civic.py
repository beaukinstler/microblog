import json
import requests
from app import app
from bleach.sanitizer import Cleaner


ELECTION_URL = "https://www.googleapis.com/civicinfo/v2/elections?key={}".format(  # noqa
        app.config['GOOGLE_CIVIC_KEY'])
VOTERINFO_URL = "https://www.googleapis.com/civicinfo/v2/voterinfo"

cleaner = Cleaner()  # for use with user address info


def get_elections():
    raw_data = requests.request('GET', ELECTION_URL,
            params={'key': app.config['GOOGLE_CIVIC_KEY']})  # noqa
    data = json.loads(raw_data.content.decode('utf-8-sig'))
    elections = [e for e in data['elections'] if e['id'] not in '2000']
    return elections


def get_voter_info(address, electionId):
    # import pdb
    # pdb.set_trace()
    raw_data = requests.request('GET', VOTERINFO_URL,
            params={'key': app.config['GOOGLE_CIVIC_KEY'],  # noqa
                    'address': cleaner.clean(address),
                    'electionId': electionId})
    data = json.loads(raw_data.content.decode('utf-8-sig'))
    polls = data['pollingLocations']
    return [p['address'] for p in polls]
