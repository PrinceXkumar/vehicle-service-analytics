from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name="services/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/customer/', views.dashboard_customer, name='dashboard_customer'),
    path('dashboard/mechanic/', views.dashboard_mechanic, name='dashboard_mechanic'),
    path('dashboard/manager/', views.dashboard_manager, name='dashboard_manager'),
    path('services/book/', views.book_service, name='services_book'),
    path('services/<int:service_id>/assign/', views.assign_mechanic, name='services_assign'),
    path('services/<int:service_id>/status/', views.update_service_status, name='services_update_status'),
    
    # Analytics URLs
    path('analytics/', views.analytics_redirect, name='analytics'),
    path('analytics/manager/', views.analytics_dashboard, name='analytics_dashboard'),
    path('analytics/customer/', views.customer_analytics, name='customer_analytics'),
    path('analytics/mechanic/', views.mechanic_analytics, name='mechanic_analytics'),
    path('analytics/api/data/', views.analytics_data_api, name='analytics_data_api'),
    path('analytics/export/', views.export_report, name='export_report'),
    
    path('', views.home, name='home'),
]
