"""Email URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from frontend import views

urlpatterns = [
    # 地址+vue中的url
    path('admin/', admin.site.urls),
    path('', views.Login),
    path('SignUp/', views.SignUp),
    path('Index/', views.Index),
    path('GET_test/',views.GET_test),
    path('POST_test/',views.POST_test),
    path('POST/',views.POST),
    path('userIdentified/', views.user_identified),
    path('userRegister/', views.register),
    path('WriteEmail/', views.WriteEmail),
    path('ReceiveEmail/', views.ReceiveEmail),
    path('SentEmail/', views.SentEmail),
    path('ChangePass/', views.ChangePass),
    path('Logout/', views.Logout),
    path('ChangePwd/', views.ChangePwd),

]
