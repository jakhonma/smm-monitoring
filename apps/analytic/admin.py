from django.contrib import admin
from .models import ChannelSocialStats, KPIFormula

@admin.register(ChannelSocialStats)
class ChannelSocialStatsAdmin(admin.ModelAdmin):
    # exclude = ('channel_social_account',)
    pass


@admin.register(KPIFormula)
class ChannelSocialStatsAdmin(admin.ModelAdmin):
    list_display = ['social_network', 'metric', 'min_value', 'points']
    list_filter = ['social_network', 'metric']
