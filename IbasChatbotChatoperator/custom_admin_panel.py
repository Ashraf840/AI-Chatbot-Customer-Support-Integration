from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import gettext as _

from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from authenticationApp import models
# from authenticationApp.admin import UserAdmin, User_ProfileAdmin, User_signin_token_tmsAdmin
