#!/usr/bin/env python3

import datetime as dt
#import os

import requests
import simplejson as json

API_URL = 'https://api.thetvdb.com'

cred = {
    'username': 'dpetrov',
    'userkey': '5C0031C22863D49B',
    'apikey': '267A2E763EBB1821',
}


class Token():

    token = ''
    date = ''

    def __init__(self, cred):
        resp = requests.post(API_URL + '/login', data=json.dumps(cred), headers={'Content-Type': 'application/json'})
        if resp.status_code == 200:
            self.token = resp.json()['token']
            self.date = dt.datetime.now()
        else:
            raise Exception('Could not acquire token')


class API():

    def __init__(self, cred=cred):
        self._token = Token(cred)

    def _get_headers(self, lang='en'):
        d = {
            'Accept': 'application/json',
            'Accept-Language': lang,
            'Authorization': 'Bearer %s' % self._token.token,
        }
        return d

    def search(self, q):
        params = {'name' : q}
        res = []
        resp = requests.get(API_URL + '/search/series', params=params, headers=self._get_headers())

        if resp.status_code == 200:
            for series in resp.json()['data']:
                res.append(series)
        return res

    def get_episodes_by_id(self, ep_id, page=1):
        params = {'page': page}
        resp = requests.get(API_URL + '/series/%s/episodes' % ep_id, params=params, headers=self._get_headers())
        if resp.status_code == 200:
            return resp.json()['data']
        else:
            return []


class EpisodeIter():

    def __init__(self, api):
        self.api = api



if __name__ == '__main__':
    print('boilerplate!')
