from django.contrib import admin
from .models import Channel, SocialNetwork, ChannelSocialAccount

admin.site.register([Channel, SocialNetwork, ChannelSocialAccount])
