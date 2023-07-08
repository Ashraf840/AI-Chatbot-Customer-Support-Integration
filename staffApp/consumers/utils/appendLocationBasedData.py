
class AppendLocationBasedData:
    def __init__(self, user:object, user_organization:str, user_location:str, user_district:str,  user_division:str):
        self.user = user
        self.user_organization = user_organization
        self.user_location = user_location
        self.user_district = user_district
        self.user_division = user_division

        # if data==None check may be completed by dictionary.get(<dynamicDictKey>) function where in the value, the class methods will be called accordingly.
        # info_dict = {
        #     "phone": "Handheld communication device",
        #     "car": "Self-propelled ground vehicle",
        #     "dinosaur": "Extinct lizard"
        # }

        self.check_execute()

    def add_organization(self):
        self.user.user_organization = self.user_organization
        self.user.save()

    def add_location(self):
        self.user.location = self.user_location
        self.user.save()

    def add_district(self):
        self.user.district = self.user_district
        self.user.save()

    def add_division(self):
        self.user.division = self.user_division
        self.user.save()
    
    def check_execute(self):
        if self.user.user_organization is None:
            # append user-org-name in CSOOnline model record using the passed value (user_organization)
            self.add_organization()
            # print("user.user_organization is None")
        if self.user.location is None:
            # append user-location in CSOOnline model record using the passed value (user_location)
            self.add_location()
            # print("user.location is None")
        if self.user.district is None:
            # append user-district in CSOOnline model record using the passed value (user_district)
            self.add_district()
            # print("user.district is None")
        if self.user.division is None:
            # append user-division in CSOOnline model record using the passed value (user_division)
            self.add_division()
            # print("user.division is None")

