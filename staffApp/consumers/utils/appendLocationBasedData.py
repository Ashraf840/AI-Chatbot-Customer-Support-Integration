
class AppendLocationBasedData:
    def __init__(self, user:object, user_organization:str, user_location:str, user_district:str,  user_division:str):
        self.user = user
        self.user_organization = user_organization
        self.user_location = user_location
        self.user_district = user_district
        self.user_division = user_division

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
            self.add_organization()
        if self.user.location is None:
            self.add_location()
        if self.user.district is None:
            self.add_district()
        if self.user.division is None:
            self.add_division()

