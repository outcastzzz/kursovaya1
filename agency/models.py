from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Модель для клиентов
class Client(models.Model):
    """Клиенты рекламного агентства"""
    name = models.CharField('Название компании', max_length=200)
    contact_person = models.CharField('Контактное лицо', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    address = models.TextField('Адрес', blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Project(models.Model):
    """Проекты/кампании"""
    STATUS_CHOICES = [
        ('planning', 'Планирование'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершен'),
        ('on_hold', 'Приостановлен'),
    ]

    name = models.CharField('Название проекта', max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент', related_name='projects')
    description = models.TextField('Описание', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='planning')
    budget = models.DecimalField('Бюджет', max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField('Дата начала', default=timezone.now)
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.client.name}"

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'




class ProjectFile(models.Model):
    """Файлы, прикрепленные к проектам"""
    name = models.CharField('Название файла', max_length=200)
    file = models.FileField('Файл', upload_to='project_files/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект', related_name='files')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Загрузил')
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'







class ProjectRequest(models.Model):
            """Заявки на проекты от клиентов"""
            STATUS_CHOICES = [
                ('new', 'Новая'),
                ('in_review', 'На рассмотрении'),
                ('approved', 'Одобрена'),
                ('rejected', 'Отклонена'),
            ]

            user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',
                                     related_name='project_requests')
            company_name = models.CharField('Название компании', max_length=200)
            contact_person = models.CharField('Контактное лицо', max_length=100)
            phone = models.CharField('Телефон', max_length=20)
            email = models.EmailField('Email')
            project_name = models.CharField('Название проекта', max_length=200)
            project_description = models.TextField('Описание проекта')
            budget = models.DecimalField('Бюджет', max_digits=10, decimal_places=2, null=True, blank=True)
            status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
            created_at = models.DateTimeField('Дата создания', auto_now_add=True)

            def __str__(self):
                return f"{self.project_name} - {self.company_name}"

            class Meta:
                verbose_name = 'Заявка на проект'
                verbose_name_plural = 'Заявки на проекты'

