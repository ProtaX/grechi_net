from django.contrib import admin
from .models import VisitorData
from .models import InviteEntry

admin.site.register(VisitorData)
admin.site.register(InviteEntry)