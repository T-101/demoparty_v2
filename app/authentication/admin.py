from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from authentication.forms import BisseeUserCreationForm, BisseeUserChangeForm
from authentication.models import DemoPartyUser


class DemoPartyUserAdmin(BaseUserAdmin):
    # add_form = BisseeUserCreationForm
    # form = BisseeUserChangeForm
    model = DemoPartyUser

    list_display = BaseUserAdmin.list_display + ('scene_id', 'user_class')

    actions = ['set_infinite_ban']
    list_filter = ('user_class',) + BaseUserAdmin.list_filter
    search_fields = ['username', 'scene_id']

    fieldsets = (
                    ('Bissee info', {'fields': ('user_class', 'ban_reason', 'ban_ends')}),
                ) + BaseUserAdmin.fieldsets

    def set_infinite_ban(self, request, queryset):
        users = []
        for obj in queryset:
            obj.set_infinite_ban(reason="Banned by Admin")
            users.append(obj.username)
        self.message_user(request, f"Users {', '.join(users)} have been banned")

    set_infinite_ban.short_description = "Set INFINITE Ban to user(s)"


admin.site.register(DemoPartyUser, DemoPartyUserAdmin)
