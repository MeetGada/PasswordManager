from django.contrib import admin
from .models import *

admin.site.site_header = "Credentials Manager Admin"

class CustAdminPanel(admin.ModelAdmin):
    exclude = ('key', 'user_id', 'password')
    # fields =('name', 'description')
    list_display = ('name', 'description',)

admin.site.register(credentials, CustAdminPanel)
