from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "telephone", "date_creation")
    search_fields = ("nom", "email", "telephone")
    list_filter = ("date_creation",)
    ordering = ("-date_creation",)
