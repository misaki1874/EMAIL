import pymysql
from django.http import JsonResponse
from django.shortcuts import render

from . import models
# Create your views here.

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
# 用户管理页面
def UserManage(request):
    return render(request,'UserManage.html')


# 身份信息获取
# authority：管理员1 普通用户0
def GetIdentity(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "未登录", "status": 404})

    userId = request.session.get('userId', None)
    userName = request.session.get('userName', None)
    authorityNo = request.session.get('userAuthority', None)
    return JsonResponse({
        "message": "返回数据成功",
        "status": 200,
        "userName": userName,
        "userId": userId,
        "authorityNo": authorityNo})


# 用户注册
# 参数：用户名，密码
# 注册成功，返回消息和200状态码
# 注册失败，返回消息和404状态码
def register(request):
    # 登录状态不允许注册
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "登录状态，无法注册", "status": 404})

    userName = request.POST.get('userName',None)
    password = request.POST.get('password',None)
    userEmail = userName+'@skyfall.icu'
    sameNameUser = models.User.objects.filter(user_name=userName)
    # 用户已存在
    if sameNameUser or userName == 'admin':
        return JsonResponse({"message": "该用户名已被占用，请重新输入用户名", "status": 404})
    # 注册新用户
    models.User.objects.create(
        user_name=userName,
        user_code=password,
        user_email=userEmail,
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

    userName = request.POST.get('userName',None)
    password = request.POST.get('password',None)
    user = models.User.objects.filter(user_name=userName)
    if not user.exists():  # 无记录 不存在该用户
        return JsonResponse({"message": "用户不存在，请进行注册", "status": 404})
    # 身份验证
    user = user.first()
    userId = user.user_id
    if userName == 'admin' and password == '123456':  # 管理员
        # 设置登录状态为True，设置登录id为username
        request.session['isLogin'] = True
        request.session['userName'] = userName
        request.session['userId'] = userId
        request.session['userAuthority'] = 1
        return JsonResponse({
            "message": "登陆成功",
            "status": 200,
            "userName": userName,
            "userId": userId,
            "authorityNo": 1})
    elif user.user_code == password:  # 普通用户
        request.session['isLogin'] = True
        request.session['userName'] = userName
        request.session['userId'] = userId
        request.session['userAuthority'] = 0
        return JsonResponse({
            "message": "登陆成功",
            "status": 200,
            "userName": userName,
            "userId": userId,
            "authorityNo": 0})
    else:
        return JsonResponse({"message": "用户名或密码输入错误", "status": 404})


# 修改密码
# 参数：旧密码oldPassword，新密码newPassword
def ChangePwd(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})

    userName = request.session.get("userName", None)
    oldPassword = request.POST.get('oldPassword', None)
    newPassword = request.POST.get('newPassword', None)
    user = models.User.objects.filter(user_name=userName)
    user = user.first()
    if user.user_code != oldPassword:
        return JsonResponse({"message": "原密码错误，请重新输入", "status": 404})
    if user.user_code == newPassword:
        return JsonResponse({"message": "新密码与原密码相同，请重新输入", "status": 404})

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


# 用户管理列表
def UserList(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})
    users = models.User.objects.all().order_by("user_name")
    infoList = []
    for user in users:
        infoList.append({'userId': user.user_id,
                         'userName': user.user_name,
                         'mailAddr': user.user_email,
                         'SMTPstate': user.smtp_state,
                         'POP3state': user.pop_state})
    return JsonResponse({
        "message": "返回数据成功",
        "status": 200,
        "infoList": infoList})

# SMTP禁用
def StopSMTP(request):
    userId = request.POST.get('userId',None)
    try:
        user = models.User.objects.filter(user_id=userId)
        user = user.first()
        if user.smtp_state == 1:
            user.smtp_state = 0
            user.save()
        return JsonResponse({"message": "SMTP已禁用", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# SMTP开启
def StartSMTP(request):
    userId = request.POST.get('userId',None)
    try:
        user = models.User.objects.filter(user_id=userId)
        user = user.first()
        if user.smtp_state == 0:
            user.smtp_state = 1
            user.save()
        return JsonResponse({"message": "SMTP已开启", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# POP3禁用
def StopPOP3(request):
    userId = request.POST.get('userId',None)
    try:
        user = models.User.objects.filter(user_id=userId)
        user = user.first()
        if user.pop_state == 1:
            user.pop_state = 0
            user.save()
        return JsonResponse({"message": "POP3已禁用", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# POP3开启
def StartPOP3(request):
    userId = request.POST.get('userId',None)
    try:
        user = models.User.objects.filter(user_id=userId)
        user = user.first()
        if user.pop_state == 0:
            user.pop_state = 1
            user.save()
        return JsonResponse({"message": "POP3已开启", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# 管理员删除用户
def DeleUser(request):
    userId = request.POST.get('userId',None)
    try:
        user = models.User.objects.filter(user_id=userId)
        user = user.first()
        user.delete()
        return JsonResponse({"message": "用户已删除", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# 删除邮件
def DeleEmail(request):
    mailId = request.POST.get('mailId',None)
    try:
        email = models.Email.objects.filter(email_id=mailId)
        email = email.first()
        email.delete()
        return JsonResponse({"message": "邮件已删除", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# 发件箱列表
def SendList(request):
    userId = request.POST.get('userId',None)
    try:
        userEmail = models.User.objects.get(user_id=userId).user_email
        emails = models.Email.objects.filter(email_from=userEmail, del_flag=0).order_by("-send_time")
        infoList = []
        for email in emails:
            infoList.append({'emailId': email.email_id,
                             'emailTo': email.email_to,
                             'emailSubject': email.email_subject,
                             'sendTime': email.send_time})
        return JsonResponse({
            "message": "返回数据成功",
            "status": 200,
            "infoList": infoList})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# 收件箱列表
def RcvList(request):
    userId = request.POST.get('userId',None)
    try:
        userEmail = models.User.objects.get(user_id=userId).user_email
        emails = models.Email.objects.filter(email_to=userEmail, del_flag=0).order_by("-send_time")
        infoList = []
        for email in emails:
            infoList.append({'emailId': email.email_id,
                             'emailFrom': email.email_from,
                             'emailSubject': email.email_subject,
                             'sendTime': email.send_time})
        return JsonResponse({
            "message": "返回数据成功",
            "status": 200,
            "infoList": infoList})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})



def GET_test(request):
    return render(request,'GET_test.html')

def POST_test(request):
    return render(request,'POST_test.html')

def POST(request):
    userName=request.POST['userName']
    password=request.POST['password']
    mail=request.POST['mail']
    port=request.POST['port']
    models.User.objects.create(user_name=userName,user_code=password,user_email=mail,smtp_state='1',pop_state='1',port=port)
    return render(request,'result.html',context={'data':userName})

def GET_test(request):
    data = models.User.objects.all()
    # context必须是一个键值对
    return render(request,'GET_test.html',context={'data':data})