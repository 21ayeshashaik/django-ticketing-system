from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='tickets'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('signup/', views.signup, name='signup'),
]