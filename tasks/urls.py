from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/completed', views.tasks_completed, name='tasks_completed'),
    path('login/', views.signin, name='login'),
    path('tasks/create/', views.create_task, name='create_tasks'),
    path('tasks/detail/<int:id>', views.task_detail, name='task_detail'),
    path('tasks/detail/complete/<int:id>', views.task_complete, name='task_complete'),
    path('tasks/detail/delete/<int:id>', views.task_delete, name='task_delete'),
]