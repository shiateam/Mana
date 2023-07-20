from django.contrib import admin
from .models import User, ValidationCode
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1'),
        }),
    )

class ValidationCodesAdmin(admin.ModelAdmin):
    list_display = ('id','mobile','validation_code')
    search_fields = ('id','mobile','validation_code')
    
admin.site.register(ValidationCode,ValidationCodesAdmin)