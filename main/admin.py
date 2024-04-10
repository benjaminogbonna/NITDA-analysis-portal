from django.contrib import admin
from .models import Department, Program

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    ordering = ('-date_uploaded',)
    list_display = ['program', 'department', 'year', 'date_uploaded']
    search_fields = ['program', 'department']
    list_filter = ['department', 'year']
    prepopulated_fields = {'slug': ('program',)}
