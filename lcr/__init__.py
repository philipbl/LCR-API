#!/usr/bin/env python3

import logging
import requests

_LOGGER = logging.getLogger(__name__)
HOST = "lds.org"
BETA_HOST = "beta.lds.org"
LCR_DOMAIN = "lcr.lds.org"


if _LOGGER.getEffectiveLevel() <= logging.DEBUG:
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1


class InvalidCredentialsError(Exception):
    pass

class API():
    def __init__(self, username, password, unit_number, beta=False):
        self.unit_number = unit_number
        self.session = requests.Session()
        self.beta = beta
        self.host = BETA_HOST if beta else HOST

        self._login(username, password)


    def _login(self, user, password):
        _LOGGER.info("Logging in")

        self.session.get('https://www.lds.org/mls/mbr/')
        request = self.session.post('https://ident.lds.org/sso/UI/Login',
                                    data={'action': 'login',
                                          'IDToken1': user,
                                          'IDToken2': password,
                                          'IDButton': 'Log In',
                                          'goto': '',
                                          'gotoOnFail': '',
                                          'SunQueryParamsString': '',
                                          'encoded': 'false',
                                          'gx_charset': 'UTF-8'})

        if 'Your username or password is not recognized' in request.text:
            raise InvalidCredentialsError(
                "Username or password was not correct.")


    def _make_request(self, request):
        if self.beta:
            request['cookies'] = {'clerk-resources-beta-terms': '4.1',
                                  'clerk-resources-beta-eula': '4.2'}

        response = self.session.get(**request)
        response.raise_for_status() # break on any non 200 status
        return response

    def birthday_list(self, month, months=1):
        _LOGGER.info("Getting birthday list")
        request = {'url': 'https://{}/services/report/birthday-list'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng',
                              'month': month,
                              'months': months}}

        result = self._make_request(request)
        return result.json()


    def members_moved_in(self, months):
        _LOGGER.info("Getting members moved in")
        request = {'url': 'https://{}/mls/mbr/services/report/members-moved-in/unit/{}/{}'.format(self.host,
                                                                                                  self.unit_number,
                                                                                                  months),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()


    def members_moved_out(self, months):
        _LOGGER.info("Getting members moved out")
        request = {'url': 'https://{}/mls/mbr/services/report/members-moved-out/unit/{}/{}'.format(self.host,
                                                                                                   self.unit_number,
                                                                                                   months),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()


    def member_list(self):
        _LOGGER.info("Getting member list")
        request = {'url': 'https://{}/mls/mbr/services/report/member-list'.format(self.host),
                   'params': {'lang': 'eng',
                              'unitNumber': self.unit_number}}

        result = self._make_request(request)
        return result.json()


    def individual_photo(self, member_id):
        """
        member_id is not the same as Mrn
        """
        _LOGGER.info("Getting photo for {}".format(member_id))
        request = {'url': 'https://{}/individual-photo/{}'.format(LCR_DOMAIN, member_id),
                   'params': {'lang': 'eng',
                              'status': 'APPROVED'}}

        result = self._make_request(request)
        scdn_url = result.json()['tokenUrl']
        return self._make_request({'url': scdn_url}).content


    def callings(self):
        _LOGGER.info("Getting callings for all organizations")
        request = {'url': 'https://{}/mls/mbr/services/orgs/sub-orgs-with-callings'.format(self.host),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()
