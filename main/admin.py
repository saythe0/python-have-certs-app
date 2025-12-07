from django.contrib import admin
from django.contrib. auth.admin import UserAdmin
from . models import CustomUser, Application, Review

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'fio', 'phone', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email', 'fio', 'phone']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('fio', 'phone')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('fio', 'phone', 'email')}),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'user', 'start_date', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'start_date']
    search_fields = ['course_name', 'user__username', 'user__fio']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'course_name', 'start_date', 'payment_method')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'get_user', 'created_at']
    search_fields = ['text', 'application__course_name', 'application__user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    def get_user(self, obj):
        return obj.application.user. username
    get_user.short_description = 'Пользователь'