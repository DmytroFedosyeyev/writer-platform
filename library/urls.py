from django.urls import path
from . import views

urlpatterns = [
    path('<int:work_id>/', views.work_detail_view, name='work_detail'),
    path('<int:work_id>/edit/', views.edit_work_view, name='edit_work'),
    path('create/', views.create_work_view, name='create_work'),
    path('', views.work_list_view, name='work_list'),
    path('<int:pk>/delete/', views.WorkDeleteView.as_view(), name='work_delete'),
]
