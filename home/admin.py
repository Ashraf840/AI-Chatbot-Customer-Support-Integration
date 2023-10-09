from django.contrib import admin
from .models import ChatbotVisitorMessage, CustomerSupportRequest, CSOVisitorMessage, CSOVisitorConvoInfo, UserChatbotSocket, RemarkResolution
from .user_connectivity_models import ChatSupportUserOnline, ChatSupportUserConnectedChannels


class ChatbotVisitorMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'visitors_msg', 'bot_msg', 'client_ip', 'created_at']
    list_display_links = ['id']
    search_fields = ['id', 'client_ip', 'created_at']
    readonly_fields = ['created_at']
    list_filter = ['created_at']
    list_per_page = 15
    ordering = ['-id']


class CustomerSupportRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_ip', 'room_slug', 'visitor_session_uuid', 'registered_user_email', 'registered_user_email_normalized', 'assigned_cso', 'is_resolved', 'is_dismissed', 'is_detached', 'issue_by_oid', 'created_at']
    list_display_links = ['id']
    search_fields = list_display
    readonly_fields = ['room_slug', 'visitor_session_uuid', 'created_at']
    list_filter = ['is_resolved', 'is_dismissed', 'is_detached', 'created_at']
    list_per_page = 15
    ordering = ['-id']


class CSOVisitorMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'user_identity', 'room_slug', 'created_at']
    list_display_links = ['id']
    search_fields = list_display
    readonly_fields = ['room_slug', 'created_at']
    list_filter = ['user_identity', 'created_at']
    list_per_page = 15
    ordering = ['-id']


class CSOVisitorConvoInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_slug', 'cso_email', 'registered_user_email', 'is_resolved', 'is_dismissed', 'is_connected', 'is_cancelled', 'is_cleared', 'created_at']
    list_display_links = ['id']
    search_fields = list_display[:-1]
    readonly_fields = ['created_at']
    list_filter = ['is_resolved', 'is_dismissed', 'is_connected', 'is_cancelled', 'is_cleared', 'created_at']
    list_per_page = 15
    ordering = ['-id']


class ChatSupportUserOnlineAdmin(admin.ModelAdmin):
    list_display = ['id', 'cso_email', 'visitor_session_uuid', 'room_slug', 'is_active', 'joined_at', 'last_update',]
    list_display_links = ['id']
    search_fields = list_display[:-3]
    readonly_fields = ['room_slug', 'joined_at', 'last_update',]
    list_filter = ['is_active', 'joined_at', 'last_update',]
    list_per_page = 15
    ordering = ['-id']


class ChatSupportUserConnectedChannelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'cso_email', 'visitor_session_uuid', 'room_slug', 'channel_value',]
    list_display_links = ['id']
    search_fields = list_display
    readonly_fields = ['room_slug', 'channel_value',]
    list_per_page = 15
    ordering = ['-id']


class UserChatbotSocketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'chatbot_socket_id', 'created_at']
    list_display_links = ['id']
    search_fields = list_display
    readonly_fields = ['created_at']
    list_per_page = 15
    ordering = ['-id']


class RemarkResolutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'cso_user_convo', 'remarks', 'created_at']
    list_display_links = ['id']
    search_fields = list_display
    readonly_fields = ['created_at']
    list_per_page = 15
    ordering = ['-id']


admin.site.register(ChatbotVisitorMessage, ChatbotVisitorMessageAdmin)
admin.site.register(CustomerSupportRequest, CustomerSupportRequestAdmin)
admin.site.register(CSOVisitorMessage, CSOVisitorMessageAdmin)
admin.site.register(CSOVisitorConvoInfo, CSOVisitorConvoInfoAdmin)
admin.site.register(UserChatbotSocket, UserChatbotSocketAdmin)
admin.site.register(RemarkResolution, RemarkResolutionAdmin)

# User online connectivity models
admin.site.register(ChatSupportUserOnline, ChatSupportUserOnlineAdmin)
admin.site.register(ChatSupportUserConnectedChannels, ChatSupportUserConnectedChannelsAdmin)
