from django.contrib import admin
from django.contrib.auth.models import Group
from list.models import Task, Tag


admin.site.register(Tag)
admin.site.register(Task)
admin.site.unregister(Group)
