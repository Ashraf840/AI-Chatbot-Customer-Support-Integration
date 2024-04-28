from django.shortcuts import redirect
from django.contrib.auth import login


def userRoleCheck(userInstance):
    if userInstance.is_cso:
        print("User is a CSO! Redirect to the CSO login page, it'll trigger the get() func of 'CSOLoginPageView' class")
    
    if userInstance.is_user:
        print("User is an iBAS++ user! Redirect to the User login page, it'll trigger the get() func of 'UserLoginPageView' class")

