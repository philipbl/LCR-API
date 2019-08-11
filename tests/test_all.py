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
                         "id", "unitName", "outOfUnitMember", "displayBirthdate", 
                         "birthDaySort", "birthDayFormatted", "birthDateFormatted"}
        actual_keys = set(birthday.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_moveins(self):
        moveins = Test.cd.members_moved_in(5)
        assert isinstance(moveins, list)

        movein = moveins[0]
        assert isinstance(movein, dict)

        expected_keys = {"moveDateOrder", "priesthood", "householdPosition", "birthdateCalc",
                         "name", "phone", "addressUnknown",
                         "priorUnitNumber", "age", "unitName",
                         "householdPositionEnum", "genderLabelShort", "locale",
                         "textAddress", "householdUuid", "nameOrder",
                         "id", "moveDateCalc", "priorUnitName", "moveDate",
                         "gender", "address", "birthdate"}
        actual_keys = set(movein.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_moveouts(self):
        moveouts = Test.cd.members_moved_out(5)
        assert isinstance(moveouts, list)

        moveout = moveouts[0]
        assert isinstance(moveout, dict)

        expected_keys = {"deceased", "nextUnitNumber", "name", "nextUnitName",
                         "addressUnknown", "moveDate", "priorUnit",
                         "moveDateOrder", "birthDate", "nameOrder"}
        actual_keys = set(moveout.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_ministering(self):
        ministering = Test.cd.ministering()
        assert isinstance(ministering, dict)

        eq = ministering['elders']
        assert isinstance(eq, list)

        rs = ministering['reliefSociety']
        assert isinstance(rs, list)

    def test_member_list(self):
        member_list = Test.cd.member_list()

        assert isinstance(member_list, list)

        member = member_list[0]
        assert isinstance(member, dict)

        expected_keys = {
            'legacyCmisId', 'householdRole', 'unitNumber', 'personUuid', 
            'houseHoldMemberNameForList', 'age', 'unitOrgsCombined', 'isYoungSingleAdult', 
            'householdNameFamilyLocal', 'priesthoodOffice', 'email', 'householdAnchorPersonUuid',
            'membershipUnit', 'isOutOfUnitMember', 'nameGivenPreferredLocal',
            'nameFamilyPreferredLocal', 'isMember', 'birth', 'formattedAddress', 
            'householdNameDirectoryLocal', 'emails', 'nameFormats', 'nameOrder', 
            'phoneNumber', 'sex', 'address', 'member', 'convert', 'personStatusFlags', 
            'outOfUnitMember', 'nameListPreferredLocal', 'uuid', 'isHead', 
            'householdEmail', 'priesthoodTeacherOrAbove', 'householdMember', 'isSingleAdult', 
            'isSpouse', 'isAdult', 'youthBasedOnAge', 'phones', 'householdUuid', 
            'householdPhoneNumber', 'unitName', 'isProspectiveElder'}
        actual_keys = set(member.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_recommend_status(self):
        recommend_status = Test.cd.recommend_status()

        assert isinstance(recommend_status, list)

        member = recommend_status[0]
        assert isinstance(member, dict)

        expected_keys = {
                "name", "spokenName", "nameOrder", "birthDate", "birthDateSort", "gender", "genderCode",
                "mrn", "id", "email", "householdEmail", "phone", "householdPhone", "unitNumber",
                "unitName", "priesthood", "priesthoodCode", "priesthoodType", "age", "actualAge", "actualAgeInMonths",
                "genderLabelShort", "visible", "nonMember", "outOfUnitMember", "marriageDate", "endowmentDate", "expirationDate",
                "status", "recommendStatus", "type", "unordained", "notBaptized", "recommendEditable", "recommendStatusSimple",
                "formattedMrn", "setApart", "sustainedDate", "birthDayFormatted", "birthDateFormatted", "birthDaySort"
                }

        actual_keys = set(member.keys())
        self.check_keys(expected_keys, actual_keys)
