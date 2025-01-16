
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('it_dashboard/', views.it_dashboard, name='it_dashboard'),
    path('submit_ticket/', views.submit_ticket, name='submit_ticket'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('submit_ticket/', views.submit_ticket, name='submit_ticket'),
    path('assign_ticket/<int:ticket_id>/', views.assign_ticket, name='assign_ticket'),
    path('complete_ticket/<int:ticket_id>/', views.complete_ticket, name='complete_ticket'),
    path('rate_ticket/<int:ticket_id>/', views.rate_ticket, name='rate_ticket'),
    path('ticket_list/', views.ticket_list, name='ticket_list'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]
