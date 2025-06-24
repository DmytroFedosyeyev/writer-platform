from django.urls import path
from . import views

# Набор маршрутов для управления произведениями
urlpatterns = [
    # Просмотр деталей конкретного произведения по ID
    path('<int:work_id>/', views.work_detail_view, name='work_detail'),
    # Экспорт произведения в PDF по ID
    path('works/<int:work_id>/export-pdf/', views.export_work_pdf, name='export_work_pdf'),
    # Редактирование произведения по ID
    path('<int:work_id>/edit/', views.edit_work_view, name='edit_work'),
    # Создание нового произведения
    path('create/', views.create_work_view, name='create_work'),
    # Список всех произведений
    path('', views.work_list_view, name='work_list'),
    # Удаление произведения по первичному ключу
    path('<int:pk>/delete/', views.WorkDeleteView.as_view(), name='work_delete'),
]