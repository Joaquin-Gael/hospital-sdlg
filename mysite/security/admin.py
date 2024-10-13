from django.contrib import admin
from .models import BlackListTokens, SessionTokens

# Register your models here.
@admin.register(BlackListTokens)
class BlackListTokensAdmin(admin.ModelAdmin):
    list_display = ('tokenJTID', 'created_at', 'expires_at')
    search_fields = ('tokenJTID',)
    ordering = ('-created_at',)

@admin.register(SessionTokens)
class SessionTokensAdmin(admin.ModelAdmin):
    list_display = ('tokenUUID', 'created_at', 'expires_at')
    search_fields = ('tokenUUID',)
    ordering = ('-created_at',)