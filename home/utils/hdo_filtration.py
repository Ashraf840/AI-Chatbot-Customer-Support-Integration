from staffApp.cso_connectivity_models import CSOOnline

class LocationBasedActiveHDOFiltration:
    def __init__(self, active_cso, user_profile):
        self.active_cso = active_cso
        self.user_profile = user_profile
        self.filtered_result = list()
    
    def exact_match(self):
        for ac in self.active_cso:
            if ac["user_organization"] == self.user_profile.user_organization and \
                ac["location"] == self.user_profile.location and \
                ac["district"] == self.user_profile.district and \
                ac["division"] == self.user_profile.division:
                self.filtered_result.append(ac)
        return self.filtered_result
    
    def org_loc_match(self):
        for ac in self.active_cso:
            if ac["user_organization"] == self.user_profile.user_organization and ac["location"] == self.user_profile.location:
                self.filtered_result.append(ac)
        return self.filtered_result

    def org_match(self):
        for ac in self.active_cso:
            if ac["user_organization"] == self.user_profile.user_organization:
                self.filtered_result.append(ac)
        return self.filtered_result
    
    def loc_match(self):
        for ac in self.active_cso:
            if ac["location"] == self.user_profile.location:
                self.filtered_result.append(ac)
        return self.filtered_result

    def dist_match(self):
        for ac in self.active_cso:
            if ac["district"] == self.user_profile.district:
                self.filtered_result.append(ac)
        return self.filtered_result

    def div_match(self):
        for ac in self.active_cso:
            if ac["division"] == self.user_profile.division:
                self.filtered_result.append(ac)
        return self.filtered_result

    def gen_match(self):
        general_cso = CSOOnline.get_active_cso()
        for ac in general_cso:
            self.filtered_result.append(ac)
        return self.filtered_result

