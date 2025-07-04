from django.contrib import admin
from .models import Job, Category, Application, Profile

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'category', 'location')
    search_fields = ('title', 'company_name', 'description', 'location')
    list_editable = ('is_approved',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Application)
admin.site.register(Profile)
