from django.contrib import admin

# Register your models here.
from .models import Task
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'due_time')
    search_fields = ('id','title' )
    list_filter = ('due_time',)

admin.site.register (Task, TaskAdmin)