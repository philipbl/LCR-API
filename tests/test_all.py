import os
import lcr


class Test:
    @classmethod
    def setup_class(cls):
        user = os.environ.get('LDS_USER')
        password = os.environ.get('LDS_PASSWORD')
        cls.cd = lcr.API(user, password)

    def test_birthday(self):
        birthdays = Test.cd.birthday_list(4, 1)

        birthdays = birthdays[0]['birthdays']
        assert isinstance(birthdays, list)

        birthday = birthdays[0]
        assert isinstance(birthday, dict)

        for key in ['formattedBirthDate', 'age', 'formattedBirthDateFull',
                    'spokenName', 'birthDateSort', 'name']:
            assert key in birthday

    def test_moveins(self):
        moveins = Test.cd.members_moved_in()
        assert isinstance(moveins, list)

        movein = moveins[0]
        assert isinstance(movein, dict)

        for key in ["formattedMrn", "formattedMoveInDate", "birthDate",
                    "moveDateOrder", "setApart", "priesthoodType",
                    "birthDateSort", "householdPhone",
                    "formattedBirthDateFull", "priesthood", "mrn",
                    "actualAge", "outOfUnitMember", "unitNumber",
                    "sustainedDate", "nameOrder", "address", "textAddress",
                    "hohMrn", "visible", "nonMember", "gender",
                    "addressUnknown", "priorUnit", "actualAgeInMonths",
                    "householdEmail", "genderLabelShort"]:
            assert key in movein

    def test_moveouts(self):
        moveouts = Test.cd.members_moved_out()
        assert isinstance(moveouts, list)

        moveout = moveouts[0]
        assert isinstance(moveout, dict)

        for key in ["birthDate", "moveDateOrder", "formattedBirthDate",
                    "nextUnitName", "moveDateStored", "nextUnitNumber",
                    "addressUnknown", "nameOrder", "moveDate", "name",
                    "birthDateStored", "priorUnit"]:
            assert key in moveout

    def test_assignments(self):
        home_teaching = Test.cd.custom_home_and_visiting_teaching()
        assert isinstance(home_teaching, dict)

        hp = home_teaching['hp']
        assert isinstance(hp, list)

        eq = home_teaching['eq']
        assert isinstance(eq, list)

        rs = home_teaching['rs']
        assert isinstance(rs, list)

        families = home_teaching['families']
        assert isinstance(families, list)

        # Check home teaching
        # TODO: Finish

        # Check families
        for key in ["emailAddress", "address", "spouse", "phone", "children",
                    "headOfHouse", "formattedCoupleName", "homeTaughtByAuxId"]:
            assert key in families[0]
