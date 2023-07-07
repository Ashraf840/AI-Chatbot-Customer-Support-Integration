from ..models import User, User_Profile


class UserDetail:
    def __init__(self, user_email):
        pass
        self.user_email = user_email

    def user_detail(self):
        ud = User.objects.get(email=self.user_email)
        return ud

    def user_profile_detail(self):
        upd = User_Profile.objects.get(user_email=self.user_email)
        return upd

    def get_combined_detail(self):
        pass
