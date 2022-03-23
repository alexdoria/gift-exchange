from django.contrib import admin
from gifts.models import Gift

# Register your models here.
@admin.register(Gift)
class PostGift(admin.ModelAdmin):
    fields = ('user', 'group', 'short_name', 'description')

