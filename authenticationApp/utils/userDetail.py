from ..models import User, User_Profile


class UserDetail:
    def __init__(self, user_email):
        pass
        self.user_email = user_email

    def user_detail(self):
        ud = User.objects.get(email=self.user_email)
        return ud

    def user_profile_detail(self, user_email):
        upd = User_Profile.objects.filter(user_email=user_email).order_by('-id').first()
        return upd

    def get_combined_detail(self):
        pass
