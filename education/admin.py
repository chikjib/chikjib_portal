from django.contrib import admin

from education.models import Education

class EducationAdmin(admin.ModelAdmin):
    list_display = ('name','amount')
    
    
admin.site.register(Education,EducationAdmin)