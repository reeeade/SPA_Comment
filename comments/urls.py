from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('', views.list_comments, name='list'),
    path('add/', views.add_comment, name='add'),
    path('add/<int:parent_id>/', views.add_comment, name='reply'),
]
