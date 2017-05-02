# Copyright 2015 Alan Vezina. All rights reserved.
import requests


class HunterClient:
    def __init__(self, api_key, api_version='v2'):
        self.api_key = api_key
        self.api_version = api_version
        self.base_url = 'https://api.hunter.io/{}/'.format(api_version)

    def _make_request(self, url, payload):
        r = requests.get(url, params=payload)
        data = r.json()
        # Raise error if not 200 OK
        r.raise_for_status()

        return data

    def search(self, domain, limit=10, offset=0, type_=None):
        """
        Returns all the email addresses found using one given domain name, with Email Hunter's sources.
        :param domain: The domain name to check for email addresses
        :return: Dict
        """
        url = self.base_url + 'domain-search'
        payload = {'api_key': self.api_key, 'domain': domain, 'limit': limit, 'offset': offset}

        if type_:
            payload['type'] = type_

        data = self._make_request(url, payload)

        return data['data']

    def find(self, domain, first_name, last_name):
        """
        Generates the most likely email of a person from their first name, last name, and a domain name
        :param domain: The domain name to search
        :param first_name: The first name of the person to search for.
        :param last_name: The last name of the person to search for.
        :return: Dict
        """
        url = self.base_url + 'email-finder'
        payload = {'api_key': self.api_key, 'domain': domain, 'first_name': first_name, 'last_name': last_name}
        data = self._make_request(url, payload)

        return data['data']

    def verify(self, email):
        """
        Verifies if a given email address is deliverable and has been found on the Internet.
        :param email: the email address you want to check
        :return: Dict
        """
        url = self.base_url + 'email-verifier'
        payload = {'api_key': self.api_key, 'email': email}
        data = self._make_request(url, payload)

        return data['data']
