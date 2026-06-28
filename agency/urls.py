from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('clients/', views.client_list, name='client_list'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),  # Добавь эту строку

 path('logout-confirm/', views.logout_confirm, name='logout_confirm'),
path('project-request/', views.create_project_request, name='project_request'),
path('my-requests/', views.my_requests, name='my_requests'),
path('admin-requests/', views.admin_requests, name='admin_requests'),
path('update-request-status/<int:request_id>/', views.update_request_status, name='update_request_status'),
path('admin-create-project-from-request/<int:request_id>/', views.admin_create_project_from_request, name='admin_create_project_from_request'),
]