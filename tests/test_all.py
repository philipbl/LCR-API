import pytest
import os
import lcr


@pytest.mark.usefixtures('betamax_session')
class Test:
    def setup_method(self, method):
        self.user = os.environ.get('LDS_USER')
        self.password = os.environ.get('LDS_PASSWORD')

    def test_birthday(self, betamax_session):
        cd = lcr.API(self.user, self.password, betamax_session)
        birthdays = cd.birthday_list(4, 1)
        birthdays = birthdays[0]['birthdays']

        assert len(birthdays) == 40
        assert birthdays[0]['name'] == 'Mita, Jessica Lorene'

    def test_moveins(self, betamax_session):
        cd = lcr.API(self.user, self.password, betamax_session)
        moveins = cd.members_moved_in()

        address = '645 E 200 S<br />Apt 11<br />Salt Lake City, Utah 84012'
        assert len(moveins) == 15
        assert moveins[0]['address'] == address

    def test_moveouts(self, betamax_session):
        cd = lcr.API(self.user, self.password, betamax_session)
        moveouts = cd.members_moved_out()

        assert len(moveouts) == 12
        assert moveouts[0]['moveDate'] == '23 Mar 2016'

    def test_assignments(self, betamax_session):
        cd = lcr.API(self.user, self.password, betamax_session)
        home_teaching = cd.custom_home_and_visiting_teaching()

        assert len(home_teaching['hp']) == 7
        assert len(home_teaching['eq']) == 6
        assert len(home_teaching['rs']) == 8
