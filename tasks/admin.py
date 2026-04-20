from django.contrib import admin
from .models import Task #Import your Task model
# Register your models here.

#This is the line that tells the Admin panel to show your tasks
# admin.site.register(Task)

#This is a 'Decorator' that let's you customize the Dashboard
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    #This shows columns for title and status in list view
    list_display = ('title', 'is_completed', 'priority')

    #This adds a filter sidebar on the right
    list_filter = ('is_completed',)

    #This adds a search bar specifically for the admin
    search_fields = ('title',)

    #This enables users to edit a field directly from list view without clicking into task. the fields should be in the list i.e. 'list_display'
    list_editable = ('is_completed','priority')