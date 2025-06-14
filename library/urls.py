from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_work_view, name='create_work'),
    path('list/', views.work_list_view, name='work_list'),
    path('<int:work_id>/', views.work_detail_view, name='work_detail'),
    path('works/<int:work_id>/export/', views.export_work_pdf, name='export_work_pdf'),

]
