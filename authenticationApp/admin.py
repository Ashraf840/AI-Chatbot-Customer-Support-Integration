from django.contrib import admin
from .models import User, User_Profile, User_signin_token_tms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from IbasChatbotChatoperator.custom_admin_panel import custom_admin_site


class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'username', 'first_name', 'last_name', 'gender', 'phone', 'date_joined', 'last_login', 'last_update', 'is_first_login', 'is_active', 'is_staff', 'is_cso', 'is_user', 'is_admin', 'is_superuser']
    list_display_links = ['email']
    search_fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone' ]
    readonly_fields = ['password', 'initial_password', 'is_first_login', 'date_joined', 'last_login', 'last_update'] # to view these fields in the "User List" model inside the admin-panel, it's required to mention explicitly these fields as readonly fields to views the fields related to date.
    # Customize the user-detail page
    fieldsets = [
        ('User Information', {
            'fields': ('email', 'password', 'initial_password', 'username', ('first_name', 'last_name'), 'gender', 'phone', 'profile_pic'),
            'classes': ('wide',),
        }),
        ('Registration & Activity', {
            'fields': ('date_joined', 'last_login', 'last_update')
        }),
        ('Roles', {
            'fields': ('is_active', 'is_staff', 'is_cso', 'is_user', 'is_admin', 'is_superuser')
        }),
        ('Groups', {
            'fields': ('groups',),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('user_permissions',),
            'classes': ('collapse',)
        }),
    ]
    list_filter = ['gender', 'date_joined', 'last_login', 'last_update', 'is_active', 'is_staff', 'is_cso', 'is_admin', 'is_superuser']
    list_per_page = 15
    ordering = ['-date_joined']
    # Customize the user-creation page
    add_fieldsets = [
        ('User Information', {
            'fields': ('email', 'username', ('first_name', 'last_name'), 'gender', 'phone', 'is_first_login',
                'profile_pic', 
                'password1', 'password2'
                ),
            'classes': ('wide',),
        }),
        ('User Permissions', {
            'fields': ('is_active', 'is_staff', 'is_cso', 'is_user', 'is_admin', 'is_superuser'),
            'classes': ('wide',),
        })
    ]


class User_ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'user_name_bn', 'user_father_name', 'user_mother_name', 'user_NID_no', 'user_organization', 'location', 'district', 'division']
    list_display_links = ['user_email']
    search_fields = list_display
    list_per_page = 15
    ordering = ['-id']


class User_signin_token_tmsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'user_id', 'user_token', 'token_type']
    list_display_links = ['user_email']
    search_fields = list_display
    list_per_page = 15
    ordering = ['-id']

admin.site.register(User, UserAdmin)
admin.site.register(User_Profile, User_ProfileAdmin)
admin.site.register(User_signin_token_tms, User_signin_token_tmsAdmin)

