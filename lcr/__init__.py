#!/usr/bin/env python3

import requests

# import logging
# import http.client as http_client

# http_client.HTTPConnection.debuglevel = 1

__version__ = '0.1.0'

BASE_URL = "https://beta.lds.org"
MLS_URL = "{}/mls/mbr".format(BASE_URL)
HT_URL = "{}/htvt/services/v1".format(BASE_URL)
USER_AGENT = ''.join(
    ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ',
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80',
     'Safari/537.36'])


class API():
    def __init__(self, username, password, session=None):
        self.session = session
        if self.session is None:
            self.session = requests.Session()

        self._login(username, password)

    def _login(self, user, password):
        # Set up the session cookie
        self.session.get('https://www.lds.org/mls/mbr/')

        # Log in
        self.session.post('https://ident.lds.org/sso/UI/Login',
                          data={'action': 'login',
                                'IDToken1': user,
                                'IDToken2': password,
                                'IDButton': 'Log In',
                                'goto': '',
                                'gotoOnFail': '',
                                'SunQueryParamsString': '',
                                'encoded': 'false',
                                'gx_charset': 'UTF-8'})

    def _get(self, url, params=None, headers=None):
        return self.session.get(url=url, params=params, headers=headers)

    def birthday_list(self, month, months=1):
        result = self._get(
            url='{}/services/report/birthday-list'.format(MLS_URL),
            params={'lang': 'eng',
                    'month': month,
                    'months': months})

        return result.json()

    def members_moved_in(self):
        result = self._get(url='{}/report/members-moved-in'.format(MLS_URL),
                           params={'lang': 'eng'})

        result = self._get(
            url='{}/services/report/members-moved-in/unit/4022/1'.format(
                MLS_URL),
            params={'lang': 'eng'},
            headers={'Accept': 'application/json, text/plain, */*',
                     'Accept-Encoding': 'gzip, deflate, sdch',
                     'Accept-Language': 'en-US,en;q=0.8',
                     'Connection': 'keep-alive',
                     'Host': 'beta.lds.org',
                     'Referer': '{}/report/members-moved-in?lang=eng'.format(
                         MLS_URL),
                     'User-Agent': USER_AGENT})

        return result.json()

    def members_moved_out(self):
        result = self._get(url='{}/report/members-moved-out'.format(MLS_URL),
                           params={'lang': 'eng'})

        result = self._get(
            url='{}/services/report/members-moved-out/unit/4022/1'.format(
                MLS_URL),
            params={'lang': 'eng'},
            headers={'Accept': 'application/json, text/plain, */*',
                     'Accept-Encoding': 'gzip, deflate, sdch',
                     'Accept-Language': 'en-US,en;q=0.8',
                     'Connection': 'keep-alive',
                     'Host': 'beta.lds.org',
                     'Referer': '{}/report/members-moved-in?lang=eng'.format(
                         MLS_URL),
                     'User-Agent': USER_AGENT})

        return result.json()

    def custom_home_and_visiting_teaching(self):
        members = self._get(url='{}/4022/members'.format(HT_URL))
        # open("members.json", 'w').write(members.text)
        members = members.json()

        hp_data = self._get('{}/4022/districts/472432'.format(HT_URL))
        # open("hp_data.json", 'w').write(hp_data.text)
        hp_data = hp_data.json()

        eq_data = self._get('{}/4022/districts/472433'.format(HT_URL))
        # open("eq_data.json", 'w').write(eq_data.text)
        eq_data = eq_data.json()

        rs_data = self._get('{}/4022/districts/472435'.format(HT_URL))
        # open("rs_data.json", 'w').write(rs_data.text)
        rs_data = rs_data.json()

        return {"families": members['families'],
                "hp": hp_data,
                "eq": eq_data,
                "rs": rs_data}
