from django.contrib import admin
from .models import Department, Program

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['program', 'department', 'year', 'date_uploaded']
    search_fields = ['program', 'department__programs__department__name', 'description']
    list_filter = ['department', 'year']
    prepopulated_fields = {'slug': ('program',)}
    ordering = ('-date_uploaded',)
