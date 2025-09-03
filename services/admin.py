from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Vehicle, ServiceRecord, Service

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('role',)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'owner', 'make', 'model', 'year', 'mileage')
    search_fields = ('registration_number', 'vin', 'owner__username')
    list_filter = ('make', 'year')


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'service_date', 'mechanic', 'odometer_reading', 'total_cost')
    search_fields = ('vehicle__registration_number', 'mechanic__username', 'issues_reported')
    list_filter = ('service_date',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'status', 'customer', 'assigned_mechanic', 'created_at')
    list_filter = ('status', 'service_type', 'created_at')
    search_fields = ('customer__username', 'customer__email', 'assigned_mechanic__username')
    autocomplete_fields = ('customer', 'assigned_mechanic')


# Extend User admin to manage Profile inline
User = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = BaseUserAdmin.list_display + ('get_role',)

    def get_role(self, obj):
        profile = getattr(obj, 'profile', None)
        return profile.role if profile else '-'
    get_role.short_description = 'Role'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
