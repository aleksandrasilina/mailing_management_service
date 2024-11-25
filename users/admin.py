from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "get_groups",
    )
    list_display_links = (
        "id",
        "email",
    )

    @admin.display(description='группы')
    def get_groups(self, obj):
        return [group for group in obj.groups.all()]
