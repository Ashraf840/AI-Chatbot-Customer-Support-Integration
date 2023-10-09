from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User, User_Profile
from .utils.emailService import EmailService
from django.contrib.auth.hashers import make_password
import string, random, json, requests


def createCSOTMS(email, username, userNameBn, userId, initial_password, mobileNumber):
    url = "https://tms-test.celloscope.net/api/v1/user/signin"
    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "user_id": "chat.operator.system.admin",
        "password": "sa"
    })
    TMS_res = requests.post(url, headers=headers, data=payload)
    TMS_res_dict = TMS_res.json()
    user_token=TMS_res_dict['token']['access_token']

    url = "https://tms-test.celloscope.net/api/v1/add-user"

    payload = json.dumps({
        "userName": f"{username}",
        "userNameBn": f"{userNameBn}",
        "userId": f"{userId}",
        "password": f"{initial_password}",
        "email": f"{email}",
        "mobileNumber": f"{mobileNumber}",
        "resetRequired": "No",
        "roleOid": "CCA-00005",
        "extensionNumber": ""
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Authorization': f'Bearer {user_token}',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://tms-test.celloscope.net',
        'Referer': 'https://tms-test.celloscope.net/user-info/add',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    }

    TMS_res = requests.post(url, headers=headers, data=payload)
    TMS_res_dict = TMS_res.json()
    print("After creating CSO into TMS:", TMS_res_dict)
    return TMS_res_dict




def random_password(pass_size=8, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(pass_size))

@receiver(post_save, sender=User)
def user_signal(sender, instance, created, **kwargs):
    if created:
        userProfile_instance = User_Profile.objects.create(
            user_email=instance.email,
        )
        if instance.is_cso:
            user = User.objects.get(email=instance.email)
            rand_pass = random_password()
            hashed_pass = make_password(rand_pass)
            user.initial_password = rand_pass
            user.password = hashed_pass
            user.save()

            userName = instance.first_name + ' ' + instance.last_name
            print("Username:", userName)
            userNameBn = None
            userId = instance.username
            initial_password = user.initial_password
            email = instance.email
            mobileNumber = instance.phone
            if userProfile_instance.user_name_bn:
                print("Username bangla:", userProfile_instance.user_name_bn)
                userNameBn = userProfile_instance.user_name_bn
            userNameBn = "-"
            print("Username bangla (-):", userNameBn)
            print("Username:", userId)
            print("user's initial-password:", user.initial_password)
            createCSOTMS(email=email, username=userName, userNameBn=userNameBn, userId=userId, initial_password=initial_password, mobileNumber=mobileNumber)


            from_mail = "python4dia@gmail.com"
            to_mail = instance.email
            email = EmailService(from_email=from_mail, to_email=to_mail)
            email.send_mail_cso(username=instance.username, password=rand_pass)
