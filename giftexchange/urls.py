"""giftexchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# App views
from gifts import views as gifts_views
from members import views as members_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', members_views.user_dashboard, name='dashboard'),
    path('dashboard/', members_views.user_dashboard, name='dashboard'),
    path('gifts/', gifts_views.gifts_view, name='gifts'),
    path('login/', members_views.login_view, name='login'),
    path('login/<str:my_user_name>', members_views.login_view, name='login'),
    path('logout/', members_views.logout_view, name='logout'),
    path('signup/<str:mail_address>', members_views.signup_view, name='signup'),
    path('signup/', members_views.signup_view, name='signup'),
    path('delete_club/', members_views.delete_club, name='delete_club'),
    path('delete_gift/', gifts_views.delete_gift, name='delete_gift'),
    path('set_gift_clubs/', gifts_views.set_gift_clubs, name='set_gift_clubs'),
    path('invite_members/', members_views.invite_members, name='invite_members'),
    path('accept_invitation/', members_views.accept_invitation, name='accept_invitation'),
    path('sort_exchange/', members_views.sort_exchange, name='sort_exchange'),
]
