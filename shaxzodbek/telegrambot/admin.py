from django.contrib import admin
from django.utils.html import format_html
from .models import TelegramUser, UserCommands


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "first_name",
        "last_name",
        "username",
        "phone_number",
        "created_at",
        "command_count",
    )
    list_filter = ("created_at",)
    search_fields = ("user_id", "first_name", "last_name", "username", "phone_number")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def command_count(self, obj):
        count = UserCommands.objects.filter(user_id=obj).count()
        return format_html(
            '<a href="{}?user_id__user_id={}">{} commands</a>',
            "/admin/your_app_name/usercommands/",  # Replace 'your_app_name' with actual app name
            obj.user_id,
            count,
        )

    command_count.short_description = "Commands"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("usercommands_set")


@admin.register(UserCommands)
class UserCommandsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_user_name",
        "command",
        "truncated_response",
        "created_at",
    )
    list_filter = ("created_at", "command", "user_id")
    search_fields = (
        "user_id__first_name",
        "user_id__last_name",
        "user_id__username",
        "command",
        "response",
    )
    raw_id_fields = ("user_id",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_user_name(self, obj):
        if obj.user_id:
            return f"{obj.user_id.first_name} {obj.user_id.last_name or ''}"
        return "Unknown User"

    get_user_name.short_description = "User"
    get_user_name.admin_order_field = "user_id__first_name"

    def truncated_response(self, obj):
        if obj.response:
            return obj.response[:50] + "..." if len(obj.response) > 50 else obj.response
        return "-"

    truncated_response.short_description = "Response"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user_id")
