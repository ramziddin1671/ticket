from django.contrib import admin
from .models import Ticket, Profile

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_at', 'file')  # To'g'ri maydonlarni ko'rsating
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'rating')
    list_filter = ('role',)
    search_fields = ('user__username', 'role')
