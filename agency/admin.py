from django.contrib import admin
from .models import Client, Project, ProjectFile, ProjectRequest
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person', 'email')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'status', 'budget', 'start_date', 'end_date')
    list_filter = ('status', 'client')
    search_fields = ('name', 'client__name')


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'uploaded_by', 'uploaded_at')
    list_filter = ('project',)


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'project_name', 'user', 'status', 'created_at', 'create_project_button')
    list_filter = ('status', 'created_at')
    search_fields = ('company_name', 'project_name', 'user__username')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Клиент', {
            'fields': ('user', 'company_name', 'contact_person', 'phone', 'email')
        }),
        ('Проект', {
            'fields': ('project_name', 'project_description', 'budget', 'status')
        }),
        ('Даты', {
            'fields': ('created_at',)
        }),
    )

    def create_project_button(self, obj):
        """Кнопка для создания проекта из заявки"""
        if obj.status == 'approved':
            return format_html(
                '<a class="button" href="{}" style="background: #ff69b4; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none;">Создать проект</a>',
                reverse('admin_create_project_from_request', args=[obj.id])
            )
        return "—"

    create_project_button.short_description = "Действие"

    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"Заявки одобрены")
    approve_requests.short_description = "Одобрить выбранные заявки"

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"Заявки отклонены")
    reject_requests.short_description = "Отклонить выбранные заявки"