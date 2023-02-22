from django.contrib import admin
from .cso_connectivity_models import CSOOnline, CSOConnectedChannels


class CSOOnlineAdmin(admin.ModelAdmin):
    list_display = ['id', 'cso_email', 'room_slug', 'is_active', 'joined_at', 'last_update',]
    list_display_links = ['id']
    search_fields = list_display[:-3]   # except the "is_active", "joined_at" & "last_update" fields
    # readonly_fields = ['room_slug', 'created_at']
    readonly_fields = ['room_slug', 'joined_at', 'last_update',]
    list_filter = ['is_active', 'joined_at', 'last_update',]
    list_per_page = 15
    ordering = ['-id']


class CSOConnectedChannelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'cso_email', 'room_slug', 'channel_value',]
    list_display_links = ['id']
    search_fields = list_display
    readonly_fields = ['room_slug', 'channel_value',]
    list_per_page = 15
    ordering = ['-id']


admin.site.register(CSOOnline, CSOOnlineAdmin)
admin.site.register(CSOConnectedChannels, CSOConnectedChannelsAdmin)
