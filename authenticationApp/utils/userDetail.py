from ..models import User, User_Profile


class UserDetail:
    def __init__(self, user_email):
        pass
        self.user_email = user_email

    def user_detail(self):
        ud = User.objects.get(email=self.user_email)
        return ud

    def user_profile_detail(self):
        # upd = User_Profile.objects.get(user_email=self.user_email)
        # Update the previous LOC, since if there is any multiple hdo-user-profiles in the DB, it'll only fetch the latest profile among the similar the prpofile-records.
        upd = User_Profile.objects.filter(user_email='hdo1@gmail.com').order_by('-id').first()
        return upd

    def get_combined_detail(self):
        pass
