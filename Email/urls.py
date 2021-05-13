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
    path('admin/', admin.site.urls),
    path('GET_test/',views.GET_test),
    path('POST_test/',views.POST_test),
    path('POST/',views.POST),
# 登录页面
    path('', views.Login),
# 注册页面
    path('SignUp/', views.SignUp),
# 主页
    path('Index/', views.Index),
# 写邮件页面
    path('WriteEmail/', views.WriteEmail),
# 收件箱页面
    path('ReceiveEmail/', views.ReceiveEmail),
# 已发送页面
    path('SentEmail/', views.SentEmail),
# 修改密码页面
    path('ChangePass/', views.ChangePass),

# 登录认证
    path('userIdentified/', views.user_identified),
# 用户注册
    path('userRegister/', views.register),
# 登出
    path('Logout/', views.Logout),
# 修改密码
    path('ChangePwd/', views.ChangePwd),
# 身份信息获取
    path('GetIdentity/', views.GetIdentity),
# 主页收件数和发件数

# 收件箱列表

# 发件箱列表

# 具体邮件查看

]
