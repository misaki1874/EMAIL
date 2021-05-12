import pymysql
from django.http import JsonResponse
from django.shortcuts import render

from . import models
from .models import User
# Create your views here.

# 数据库连接
def connectdb():
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'maildb',
        'charset': 'utf8',
    }
    con = pymysql.connect(**config)
    return con

# 注册页面
def SignUp(request):
    return render(request,'SignUp.html')

# 登录页面
def Login(request):
    return render(request,'Login.html')

#主页
def Index(request):
    return render(request,'Index.html')

# 写邮件页面
def WriteEmail(request):
    return render(request,'WriteEmail.html')

# 收件箱页面
def ReceiveEmail(request):
    return render(request,'ReceiveEmail.html')

# 已发送页面
def SentEmail(request):
    return render(request,'SentEmail.html')

# 修改密码页面
def ChangePass(request):
    return render(request,'ChangePass.html')


# 用户注册
# 参数：用户名，密码
# 注册成功，返回消息和200状态码
# 注册失败，返回消息和404状态码
def register(request):
    # 登录状态不允许注册
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "登录状态，无法注册", "status": 404})

    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    useremail = username+'@skyfall.icu'
    sameNameUser = models.User.objects.filter(user_name=username)
    # 用户已存在
    if sameNameUser or username == 'admin':
        return JsonResponse({"message": "该用户名已被占用，请重新输入用户名", "status": 404})
    # 注册新用户
    models.User.objects.create(
        user_name=username,
        user_code=password,
        user_email=useremail,
        smtp_state='1',
        pop_state='1'
    )
    return JsonResponse({"message": "注册成功", "status": 200})


# 登录认证
# 参数：用户名, 密码
# 管理员权限No=1，普通用户权限No=0
def user_identified(request):
    # 若已经登录，直接进入已登录账号
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录", "status": 404})

    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    user = models.User.objects.filter(user_name=username)
    if not user.exists():  # 无记录 不存在该用户
        return JsonResponse({"message": "用户不存在，请进行注册", "status": 404})
    # 身份验证
    user = user.first()
    if username == 'admin' and password == '123456':  # 管理员
        # 设置登录状态为True，设置登录id为username
        request.session['isLogin'] = True
        request.session['userId'] = username
        return JsonResponse({"message": "登陆成功", "status": 200, "userId":username, "authorityNo": 1})
    elif user.user_code == password:  # 普通用户
        request.session['isLogin'] = True
        request.session['username'] = user.user_name
        return JsonResponse({"message": "登陆成功", "status": 200, "userId":username, "authorityNo": 0})
    else:
        return JsonResponse({"message": "用户名或密码输入错误", "status": 404})


# 修改密码
# 参数：用户名username，旧密码oldPassword，新密码newPassword
def ChangePwd(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})

    username = request.session.get("username", None)
    oldPassword = request.POST.get('oldPassword', None)
    newPassword = request.POST.get('newPassword', None)
    user = models.User.objects.get(user_name=username)
    if user.user_code == oldPassword:
        return JsonResponse({"message": "原密码错误，修改失败", "status": 404})

    user.user_code = newPassword
    user.save()
    return JsonResponse({"message": "修改成功", "status": 200})


# 登出
def Logout(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "未登录，无法登出", "status": 404})
    else:
        request.session.flush()
        return JsonResponse({"message": "登出成功", "status": 200})


def GET_test(request):
    return render(request,'GET_test.html')

def POST_test(request):
    return render(request,'POST_test.html')

def POST(request):
    userName=request.POST['userName']
    password=request.POST['password']
    mail=request.POST['mail']
    port=request.POST['port']
    User.objects.create(user_name=userName,user_code=password,user_email=mail,smtp_state='1',pop_state='1',port=port)
    return render(request,'result.html',context={'data':userName})

def GET_test(request):
    data = User.objects.all()
    # context必须是一个键值对
    return render(request,'GET_test.html',context={'data':data})