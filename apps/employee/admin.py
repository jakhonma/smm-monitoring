from django.contrib import admin
from .models import Employee, SMMStaff

admin.site.register([Employee, SMMStaff])
