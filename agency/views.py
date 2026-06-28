from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Client, Project, ProjectRequest
from .forms import RegisterForm, ProjectRequestForm
from django.db.models import Sum


def index(request):
    """Главная страница с дашбордом"""
    today = timezone.now().date()
    total_clients = Client.objects.count()
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='in_progress').count()
    total_budget = Project.objects.aggregate(Sum('budget'))['budget__sum'] or 0
    recent_projects = Project.objects.all().order_by('-created_at')[:6]
    for project in recent_projects:
        project.show_details = request.user.is_superuser


    context = {
        'total_clients': total_clients,
        'total_projects': total_projects,

        'active_projects': active_projects,
        'total_budget': total_budget,
        'recent_projects': recent_projects,

        'today': today,
        'is_admin': request.user.is_superuser,
    }
    return render(request, 'agency/index.html', context)


def project_list(request):
    """Страница со списком всех проектов"""
    projects = Project.objects.all().order_by('-created_at')

    context = {
        'projects': projects,
        'is_admin': request.user.is_superuser,
    }
    return render(request, 'agency/project_list.html', context)


def client_list(request):
    """Страница со списком всех клиентов"""
    clients = Client.objects.all().order_by('-created_at')

    # Считаем активные проекты (со статусом 'in_progress')
    active_projects = Project.objects.filter(status='in_progress').count()

    context = {
        'clients': clients,
        'active_projects': active_projects,
        'is_admin': request.user.is_superuser,
    }
    return render(request, 'agency/client_list.html', context)


@login_required
def profile(request):
    """Страница профиля пользователя"""
    context = {'is_admin': request.user.is_superuser}

    # Для администратора добавляем статистику
    if request.user.is_superuser:
        context['total_clients'] = Client.objects.count()
        context['total_projects'] = Project.objects.count()
        context['total_requests'] = ProjectRequest.objects.count()

    return render(request, 'agency/profile.html', context)


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'agency/register.html', {'form': form})


@login_required
def create_project_request(request):
    """Создание заявки на проект"""
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            project_request = form.save(commit=False)
            project_request.user = request.user
            project_request.save()
            messages.success(request, 'Заявка успешно отправлена! Администратор свяжется с вами.')
            return redirect('profile')
    else:
        form = ProjectRequestForm()

    return render(request, 'agency/project_request.html', {'form': form})


@login_required
def my_requests(request):
    """Список заявок пользователя"""
    requests = ProjectRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'agency/my_requests.html', {'requests': requests})


@login_required
def admin_requests(request):
    """Все заявки (только для админа)"""
    if not request.user.is_superuser:
        return redirect('profile')
    requests = ProjectRequest.objects.all().order_by('-created_at')
    return render(request, 'agency/admin_requests.html', {'requests': requests})


@login_required
def update_request_status(request, request_id):
    """Обновление статуса заявки (только для админа)"""
    if not request.user.is_superuser:
        return redirect('profile')

    project_request = get_object_or_404(ProjectRequest, id=request_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        project_request.status = status
        project_request.save()
        messages.success(request, f'Статус заявки изменен на {project_request.get_status_display()}')

    return redirect('admin_requests')


def logout_confirm(request):
    """Страница подтверждения выхода"""
    return render(request, 'agency/logout.html')


def admin_create_project_from_request(request, request_id):
    """Создание проекта из одобренной заявки (для админки)"""
    if not request.user.is_superuser:
        return redirect('profile')

    project_request = get_object_or_404(ProjectRequest, id=request_id)

    # Создаем клиента, если его нет
    client, created = Client.objects.get_or_create(
        name=project_request.company_name,
        defaults={
            'contact_person': project_request.contact_person,
            'phone': project_request.phone,
            'email': project_request.email,
        }
    )

    # Создаем проект
    project = Project.objects.create(
        name=project_request.project_name,
        client=client,
        description=project_request.project_description,
        budget=project_request.budget,
        status='planning',
        start_date=timezone.now().date(),
    )

    messages.success(request, f'Проект "{project.name}" успешно создан!')

    # Перенаправляем на страницу редактирования созданного проекта
    return redirect(f'/admin/agency/project/{project.id}/change/')