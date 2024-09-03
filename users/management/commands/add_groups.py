from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

import json


class Command(BaseCommand):
    """Команда для добавления групп пользователей"""

    @staticmethod
    def json_read_groups():
        groups = []
        with open("groups.json", "r", encoding="utf-8") as file:
            for group in json.load(file):
                if group["model"] == "auth.group":
                    groups.append(group["fields"])
        return groups

    def handle(self, *args, **options):
        groups = Command.json_read_groups()
        for group in groups:
            new_group, created = Group.objects.get_or_create(name=group["name"])
            for pk in group["permissions"]:
                proj_add_perm = Permission.objects.get(pk=pk)
                new_group.permissions.add(proj_add_perm)

        print("Groups created successfully!")