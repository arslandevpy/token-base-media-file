from django.contrib import admin
from .models import PrivateFile, PrivateFileToken


admin.site.register(PrivateFile)
admin.site.register(PrivateFileToken)
