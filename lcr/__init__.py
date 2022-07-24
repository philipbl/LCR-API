#!/usr/bin/env python3

import re
import json
import logging
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager

_LOGGER = logging.getLogger(__name__)
HOST = "churchofjesuschrist.org"
BETA_HOST = f"beta.{HOST}"
LCR_DOMAIN = f"lcr.{HOST}"
CHROME_OPTIONS = webdriver.chrome.options.Options()
CHROME_OPTIONS.add_argument("--headless")
TIMEOUT = 10


if _LOGGER.getEffectiveLevel() <= logging.DEBUG:
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1


class InvalidCredentialsError(Exception):
    pass


class API():
    def __init__(
            self, username, password, unit_number, beta=False,
            driver=webdriver.Chrome(ChromeDriverManager().install())):
        self.unit_number = unit_number
        self.session = requests.Session()
        self.driver = driver
        self.beta = beta
        self.host = BETA_HOST if beta else HOST

        self._login(username, password)

    def _login(self, user, password):
        _LOGGER.info("Logging in")

        # Navigate to the login page
        self.driver.get(f"https://{LCR_DOMAIN}")

        # Enter the username
        login_input = WebDriverWait(self.driver, TIMEOUT).until(
                        ec.presence_of_element_located(
                            (By.CSS_SELECTOR, "input#okta-signin-username")
                            )
                        )
        login_input.send_keys(user)
        login_input.submit()

        # Enter password
        password_input = WebDriverWait(self.driver, TIMEOUT).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, "input.password-with-toggle")
                    )
                )
        password_input.send_keys(password)
        password_input.submit()

        # Wait until the page is loaded
        WebDriverWait(self.driver, TIMEOUT).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, "churchofjesuschrist-eden-normalize")
                    )
                )

        # Get authState parameter.
        cookies = self.driver.get_cookies()
        potential_cookie = [c for c in cookies if "ChurchSSO" in c['name']]
        real_cookie = next(iter(potential_cookie))
        churchcookie = real_cookie['value']

        self.session.cookies['ChurchSSO'] = churchcookie
        self.driver.close()
        self.driver.quit()

    def _make_request(self, request):
        if self.beta:
            request['cookies'] = {'clerk-resources-beta-terms': '4.1',
                                  'clerk-resources-beta-eula': '4.2'}

        response = self.session.get(**request)
        response.raise_for_status()  # break on any non 200 status
        return response

    def birthday_list(self, month, months=1):
        _LOGGER.info("Getting birthday list")
        request = {
                'url': 'https://{}/services/report/birthday-list'.format(
                    LCR_DOMAIN
                    ),
                'params': {
                    'lang': 'eng',
                    'month': month,
                    'months': months
                    }
                }

        result = self._make_request(request)
        return result.json()

    def members_moved_in(self, months):
        _LOGGER.info("Getting members moved in")
        request = {'url': 'https://{}/services/report/members-moved-in/unit/{}/{}'.format(LCR_DOMAIN,
                                                                                                  self.unit_number,
                                                                                                  months),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()


    def members_moved_out(self, months):
        _LOGGER.info("Getting members moved out")
        request = {'url': 'https://{}/services/report/members-moved-out/unit/{}/{}'.format(LCR_DOMAIN,
                                                                                                   self.unit_number,
                                                                                                   months),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()


    def member_list(self):
        _LOGGER.info("Getting member list")
        request = {'url': 'https://{}/services/umlu/report/member-list'.format(LCR_DOMAIN),
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
        request = {'url': 'https://{}/services/orgs/sub-orgs-with-callings'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()


    def members_alt(self):
        _LOGGER.info("Getting member list")
        request = {'url': 'https://{}/services/umlu/report/member-list'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng',
                              'unitNumber': self.unit_number}}

        result = self._make_request(request)
        return result.json()


    def ministering(self):
        """
        API parameters known to be accepted are lang type unitNumber and quarter.
        """
        _LOGGER.info("Getting ministering data")
        request = {'url': 'https://{}/services/umlu/v1/ministering/data-full'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng',
                              'unitNumber': self.unit_number}}

        result = self._make_request(request)
        return result.json()


    def access_table(self):
        """
        Once the users role id is known this table could be checked to selectively enable or disable methods for API endpoints.
        """
        _LOGGER.info("Getting info for data access")
        request = {'url': 'https://{}/services/access-table'.format(LCR_DOMAIN),
                   'params': {'lang': 'eng'}}

        result = self._make_request(request)
        return result.json()

    def recommend_status(self):
        """
        Obtain member information on recommend status
        """
        _LOGGER.info("Getting recommend status")
        request = {
                'url': 'https://{}/services/recommend/recommend-status'.format(LCR_DOMAIN),
                'params': {
                    'lang': 'eng',
                    'unitNumber': self.unit_number
                    }
                }
        result = self._make_request(request)
        return result.json()
