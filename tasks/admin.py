from django.contrib import admin
from .models import task

# Register your models here.
class taskadmin(admin.ModelAdmin):
    readonly_fields = ('created', )

admin.site.register(task, taskadmin)
