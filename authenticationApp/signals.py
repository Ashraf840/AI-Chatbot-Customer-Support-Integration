from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User
from .utils.emailService import EmailService
from django.contrib.auth.hashers import make_password
import string, random


def random_password(pass_size=8, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(pass_size))

@receiver(post_save, sender=User)
def user_signal(sender, instance, created, **kwargs):
    if created:
        if instance.is_cso:
            # TODO: make the emails dynamic, getting from signal's instance (user-input)
            # TODO: make dediacated email template from CSOs
            # TODO: define  user_pass as instance.initial_password
            user = User.objects.get(email=instance.email)
            rand_pass = random_password()
            hashed_pass = make_password(rand_pass)  # [Ref]: https://stackoverflow.com/a/43793754
            # print('hashed pass:', hashed_pass)
            user.initial_password = rand_pass
            user.password = hashed_pass
            user.save()
            # Send Email - here
            from_mail = "python4dia@gmail.com"
            # to_mail = "enamulmajid021@gmail.com"
            to_mail = instance.email
            email = EmailService(from_email=from_mail, to_email=to_mail)
            email.send_mail_cso(username=instance.username, password=rand_pass)


