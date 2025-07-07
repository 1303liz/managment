from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'user_type', 'is_email_verified', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_email_verified', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Other', {'fields': ('user_type', 'is_email_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'user_type', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'birth_date', 'phone_number')
    search_fields = ('user__email', 'user__username')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
