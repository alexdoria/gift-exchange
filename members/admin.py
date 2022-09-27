from django.contrib import admin
from .models import Member, Club


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'club_admin',)