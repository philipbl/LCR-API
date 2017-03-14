import os
import lcr


class Test:
    @classmethod
    def setup_class(cls):
        user = os.environ['LDS_USER']
        password = os.environ['LDS_PASSWORD']
        unit_number = os.environ['LDS_UNIT_NUMBER']
        cls.cd = lcr.API(user, password, unit_number)

    def check_keys(self, expected, actual):
        if expected != actual:
            message = "Difference between expected and actual: {}\n".format(expected - actual)
            message += "Difference between actual and expected: {}\n".format(actual - expected)
            message += "Actual: {}\n".format(actual)
            assert False, message

    def test_birthday(self):
        birthdays = Test.cd.birthday_list(4, 1)

        birthdays = birthdays[0]['birthdays']
        assert isinstance(birthdays, list)

        birthday = birthdays[0]
        assert isinstance(birthday, dict)

        expected_keys = {"unitNumber", "formattedMrn", "priesthood", "mrn",
                         "actualAge", "actualAgeInMonths", "monthInteger",
                         "email", "genderCode", "birthDateSort", "age",
                         "birthDayAge", "birthDate", "nonMember", "visible",
                         "gender", "dayInteger", "address", "sustainedDate",
                         "householdEmail", "phone", "spokenName", "name",
                         "setApart", "priesthoodCode", "priesthoodType",
                         "nameOrder", "householdPhone", "genderLabelShort",
                         "id", "unitName", "outOfUnitMember"}
        actual_keys = set(birthday.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_moveins(self):
        moveins = Test.cd.members_moved_in()
        assert isinstance(moveins, list)

        movein = moveins[0]
        assert isinstance(movein, dict)

        expected_keys = {"genderCode", "priesthoodCode", "hohMrn", "visible",
                         "age", "gender", "actualAgeInMonths",
                         "outOfUnitMember", "moveDateOrder", "priesthood",
                         "householdPosition", "email", "unitName",
                         "priorUnitName", "unitNumber", "priesthoodType",
                         "nameOrder", "address", "deceased", "name",
                         "birthDateSort", "nonMember", "householdPhone",
                         "genderLabelShort", "priorUnit", "setApart",
                         "textAddress", "id", "actualAge", "moveDate",
                         "householdEmail", "addressUnknown", "spokenName",
                         "birthDate", "sustainedDate", "mrn", "formattedMrn",
                         "phone"}
        actual_keys = set(movein.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_moveouts(self):
        moveouts = Test.cd.members_moved_out()
        assert isinstance(moveouts, list)

        moveout = moveouts[0]
        assert isinstance(moveout, dict)

        expected_keys = {"deceased", "nextUnitNumber", "name", "nextUnitName",
                         "addressUnknown", "moveDate", "priorUnit",
                         "moveDateOrder", "birthDate", "nameOrder"}
        actual_keys = set(moveout.keys())
        self.check_keys(expected_keys, actual_keys)

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

        family = families[0]
        assert isinstance(family, dict)

        # Check families
        expected_keys = {"address", "responsibleHTAuxiliaryId", "spouse",
                         "isAssignedHT", "children", "headOfHouse",
                         "emailAddress", "formattedCoupleName", "phone"}
        actual_keys = set(family.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_member_list(self):
        member_list = Test.cd.member_list()

        assert isinstance(member_list, list)

        member = member_list[0]
        assert isinstance(member, dict)

        expected_keys = {"outOfUnitMember", "setApart", "priesthoodCode", "id", "name",
                         "gender", "formattedMrn", "isSpouse", "sustainedDate", "mrn",
                         "unitName", "priesthoodType", "spokenName", "householdPhone",
                         "visible", "priesthood", "nonMember", "isAdult", "birthDateSort",
                         "isHead", "birthDate", "genderLabelShort",
                         "genderCode", "actualAge", "phone", "householdEmail",
                         "actualAgeInMonths", "householdId", "coupleName",
                         "nameOrder", "givenName", "email", "unitNumber",
                         "fullTimeMissionary", "address", "age"}
        actual_keys = set(member.keys())
        self.check_keys(expected_keys, actual_keys)
