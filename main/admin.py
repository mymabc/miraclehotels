from django.contrib import admin
from .models import Crew, Customer, JobOpening

class CrewAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email', 'phone']
    search_fields = ['name', 'role', 'email']
    list_filter = ['role']
    ordering = ['name']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    search_fields = ['name', 'email']
    ordering = ['name']

class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'is_active']
    search_fields = ['title', 'description']
    list_filter = ['is_active']
    ordering = ['title']

# Explicit registration
admin.site.register(Crew, CrewAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(JobOpening, JobOpeningAdmin)
