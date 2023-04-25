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


# NOT USING THIS CLASS
# class CustomAdminSite(admin.AdminSite):
#     index_title = "Integrated Budget & Accounting System"
#     site_header = "iBAS++ Administration"
#     site_title = "iBAS++ Administration"

#     @method_decorator(never_cache)
#     def login(self, request, extra_context=None):
#         """
#         Display the login form for the given HttpRequest.
#         """
#         if request.method == "GET" and self.has_permission(request):
#             # Already logged-in, redirect to admin index
#             index_path = reverse("admin:index", current_app=self.name)
#             return HttpResponseRedirect(index_path)

#         # Since this module gets imported in the application's root package,
#         # it cannot import models from other applications at the module level,
#         # and django.contrib.admin.forms eventually imports User.
#         from django.contrib.admin.forms import AdminAuthenticationForm
#         from django.contrib.auth.views import LoginView

#         # print("\n"*3)
#         # print("#"*50)
#         # print("Custom django administration panel's login() function is called!")
#         # print("#"*50)
#         # print("\n"*3)

#         context = {
#             **self.each_context(request),
#             "title": _("Log in"),
#             "subtitle": None,
#             "app_path": request.get_full_path(),
#             "username": request.user.get_username(),
#         }
#         if (
#             REDIRECT_FIELD_NAME not in request.GET
#             and REDIRECT_FIELD_NAME not in request.POST
#         ):
#             context[REDIRECT_FIELD_NAME] = reverse("admin:index", current_app=self.name)
#         context.update(extra_context or {})

#         defaults = {
#             "extra_context": context,
#             "authentication_form": self.login_form or AdminAuthenticationForm,
#             "template_name": self.login_template or "admin/login.html",
#         }
#         request.current_app = self.name
#         return LoginView.as_view(**defaults)(request)

# custom_admin_site = CustomAdminSite(name='ibas_admin')



# custom_admin_site.register(Group, GroupAdmin)
# custom_admin_site.register(models.User)
# custom_admin_site.register(models.User_Profile)
# custom_admin_site.register(models.User_signin_token_tms)





# custom_admin_site.register(User)

# @custom_admin_site.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     search_fields = ('name',)
#     ordering = ('name',)
#     filter_horizontal = ('permissions',)

#     def formfield_for_manytomany(self, db_field, request=None, **kwargs):
#         if db_field.name == 'permissions':
#             qs = kwargs.get('queryset', db_field.remote_field.model.objects)
#             # Avoid a major performance hit resolving permission names which
#             # triggers a content_type load:
#             kwargs['queryset'] = qs.select_related('content_type')
#         return super().formfield_for_manytomany(db_field, request=request, **kwargs)

