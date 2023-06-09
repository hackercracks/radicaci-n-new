from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from filed.views import DashboardView, landingpage

urlpatterns = [
 # post views
# path('dashboard', views.dashboard, name='dashboard'),
path('dashboard/', DashboardView.as_view(), name='dashboard'),
# path('', views.landingPage, name='landpage'),
path('', landingpage, name='land-page'),

# django in built auth
# path('', auth_views.LoginView.as_view(), name='login'),
path('login/', views.user_login, name='login'),

path('logout/', auth_views.LogoutView.as_view(), name='logout'),
path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


path('register/', views.register, name='register'),
path('edit/', views.edit, name='edit'),

]