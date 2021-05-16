from datetime import datetime

import pymysql
from django.db.models import Q
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
# 后台主界面
def AdminIndex(request):
    return render(request,'AdminIndex.html')
# 邮件管理界面
def EmailManage(request):
    return render(request,'EmailManage.html')

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
        "userId": userId,
        "userName": userName,
        "authorityNo": authorityNo})


# 用户注册
# 参数：用户名，密码
def register(request):
    # 登录状态不允许注册
    if request.session.get('isLogin', None) and request.session.get('userAuthority') == 0:
        return JsonResponse({"message": "普通用户登录状态，无法注册", "status": 404})

    userName = request.POST.get('userName',None)
    password = request.POST.get('password',None)
    userEmail = userName+'@skyfall.icu'
    sameNameUser = models.User.objects.filter(user_name=userName)
    # 用户已存在
    if sameNameUser:
        return JsonResponse({"message": "该用户名已被占用，请重新输入用户名", "status": 404})
    # 注册新用户
    models.User.objects.create(
        user_name=userName,
        user_code=password,
        user_email=userEmail,
    )
    return JsonResponse({"message": "注册成功", "status": 200})


# 登录认证
# 参数：userName, password
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
    if user.user_code == password:
        # 设置登录状态为True
        request.session['isLogin'] = True
        request.session['userId'] = user.user_id
        request.session['userName'] = userName
        request.session['userAuthority'] = user.authorityNo
        return JsonResponse({
            "message": "登陆成功",
            "status": 200,
            "userName": userName,
            "userId": user.user_id,
            "authorityNo": user.authorityNo})
    else:
        return JsonResponse({"message": "用户名或密码输入错误", "status": 404})


# 修改密码
# 参数：oldPassword, newPassword
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
    managerId = request.session.get('userId')
    try:
        users = models.User.objects.exclude(user_id=managerId).order_by("user_name")
        infoList = []
        for user in users:
            infoList.append({'userId': user.user_id,
                             'userName': user.user_name,
                             'mailAddr': user.user_email,
                             'SMTPstate': user.smtp_state,
                             'POP3state': user.pop_state,
                             'authorityNo': user.authorityNo})
        return JsonResponse({
            "message": "返回数据成功",
            "status": 200,
            "infoList": infoList})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# SMTP禁用
# 参数：userId
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
# 参数：userId
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
# 参数：userId
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
# 参数：userId
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
# 参数：userId
def DeleUser(request):
    userId = request.POST.get('userId',None)
    try:
        user = models.User.objects.filter(user_id=userId)
        user = user.first()
        user.delete()
        return JsonResponse({"message": "用户已删除", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 管理员删除邮件
# 参数：mailId
def ManagerDeleEmail(request):
    mailId = request.POST.get('mailId',None)
    try:
        email = models.Email.objects.get(email_id=mailId)
        email.delete()
        return JsonResponse({"message": "邮件已删除", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 设为管理员
# 参数：userId
def SetAsManager(request):
    userId = request.POST.get('userId',None)
    try:
        user = models.User.objects.get(user_id=userId)
        user.authorityNo = 1
        user.save()
        return JsonResponse({"message": "已设为管理员", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# 设为普通用户
# 参数：userId
def SetAsUser(request):
    userId = request.POST.get('userId',None)
    try:
        user = models.User.objects.get(user_id=userId)
        user.authorityNo = 0
        user.save()
        return JsonResponse({"message": "已设为普通用户", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 邮件管理列表
def EmailList(request):
    try:
        emails = models.Email.objects.all().order_by("-send_time")
        infoList = []
        for email in emails:
            infoList.append({'emailId': email.email_id,
                             'fromAddr': email.email_from,
                             'toAddr': email.email_to,
                             'emailSubject': email.email_subject,
                             'sendTime': email.send_time})
        return JsonResponse({
            "message": "返回数据成功",
            "status": 200,
            "infoList": infoList})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})




# 发件箱列表
def SendList(request):
    userId = request.session.get('userId',None)
    try:
        userEmail = models.User.objects.get(user_id=userId).user_email
        emails = models.Email.objects.filter(email_from=userEmail, sender_del_flag=0).order_by("-send_time")
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
    userId = request.session.get('userId',None)
    try:
        user = models.User.objects.get(user_id=userId)
        if user.pop_state == 0:
            return JsonResponse({"message": "无pop权限，无法获取邮件", "status": 404})

        userEmail = user.user_email
        emails = models.Email.objects.filter(email_to=userEmail, rcver_del_flag=0).order_by("-send_time")
        infoList = []
        for email in emails:
            infoList.append({'emailId': email.email_id,
                             'emailFrom': email.email_from,
                             'emailSubject': email.email_subject,
                             'sendTime': email.send_time,
                             'readState': email.rcver_fr_flag})  # 读取状态
        return JsonResponse({
            "message": "返回数据成功",
            "status": 200,
            "infoList": infoList})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 普通用户发件箱删除邮件
# 参数：mailId
def SenderDeleEmail(request):
    mailId = request.POST.get('mailId',None)
    try:
        email = models.Email.objects.get(email_id=mailId)
        email.sender_del_flag = 1  # 当前用户为发件人
        email.sender_del_time = datetime.now()
        email.save()
        return JsonResponse({"message": "邮件已删除", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 普通用户收件箱删除邮件
# 参数：mailId
def RcverDeleEmail(request):
    mailId = request.POST.get('mailId',None)
    try:
        email = models.Email.objects.get(email_id=mailId)
        email.rcver_del_flag = 1  # 当前用户为收件人
        email.rcver_del_time = datetime.now()
        email.save()
        return JsonResponse({"message": "邮件已删除", "status": 200})
    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})



# 发邮件，含群发
# 参数：用"@skyfall.icu; "分隔的接收人邮箱字符串rcverEmailList，主题subject，内容cont
def SendEmail(request):
    rcverEmailList = request.POST.get('rcverEmailList', None)
    rcverEmailList = rcverEmailList.split('; ')
    rcverEmailList.pop()
    subject = request.POST.get("subject", None)
    cont = request.POST.get('cont',None)
    userId = request.session.get('userId')
    try:
        user = models.User.objects.get(user_id=userId)
        if user.smtp_state == 0:
            return JsonResponse({"message": "无smtp权限，无法发送邮件", "status": 404})

        for i in range(len(rcverEmailList)):  # 检查收件人存在
            rcver = models.User.objects.filter(user_email=rcverEmailList[i])
            if not rcver.exists():
                return JsonResponse({"message": "有用户不存在，发送失败", "status": 404})

        for i in range(len(rcverEmailList)):  # 发邮件
            rcver = models.User.objects.get(user_email=rcverEmailList[i])
            print(rcver.user_email)
            models.Email.objects.create(
                email_from=user.user_email,
                email_to=rcver.user_email,
                email_subject=subject,
                email_cont=cont,
                send_time=datetime.now(),
                email_size=len(cont)
            )
        return JsonResponse({"message": "邮件发送成功", "status": 200})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# 具体邮件查看
# 参数：mailId
def CheckMail(request):
    mailId = request.POST.get('mailId',None)
    authorityNo = request.session.get('userAuthority',None)
    try:
        email = models.Email.objects.get(email_id=mailId)
        if authorityNo == 0 and email.rcver_fr_flag == 0:  # 普通用户第一次读取该邮件
            email.rcver_fr_flag = 1
            email.rcver_fr_time = datetime.now()
            email.pop_log = 1  # 加入pop日志
            email.save()

        info = {}
        info['emailId'] = email.email_id
        info['fromAddr'] = email.email_from
        info['toAddr'] = email.email_to
        info['emailSubject'] = email.email_subject
        info['emailCont'] = email.email_cont
        info['sendTime'] = email.send_time
        return JsonResponse({"message": "返回数据成功", "status": 200, "info": info})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# SMTP日志列表
def SMTPLogList(request):
    infoList = []
    try:
        emails = models.Email.objects.filter(smtp_log=1).order_by("-send_time")
        for email in emails:
            infoList.append({'emailId': email.email_id,
                             'fromAddr': email.email_from,
                             'toAddr': email.email_to,
                             'emailSubject': email.email_subject,
                             'sendTime': email.send_time,
                             })
        return JsonResponse({"message": "返回数据成功", "status": 200, "infoList": infoList})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# POP日志列表
def POPLogList(request):
    infoList = []
    try:
        emails = models.Email.objects.filter(pop_log=1).order_by("-rcver_fr_time")
        for email in emails:
            infoList.append({'emailId': email.email_id,
                             'fromAddr': email.email_from,
                             'toAddr': email.email_to,
                             'emailSubject': email.email_subject,
                             'readTime': email.rcver_fr_time,  # 读取时间
                             })
        return JsonResponse({"message": "返回数据成功", "status": 200, "infoList": infoList})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# SMTP日志清除
# 参数：mailId
def DeleSMTPLog(request):
    emailId = request.POST.get("mailId")
    try:
        email = models.Email.objects.get(email_id=emailId)
        email.smtp_log = 0
        email.save()
        return JsonResponse({"message": "日志清除成功", "status": 200})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})

# POP日志清除
# 参数：mailId
def DelePOPLog(request):
    emailId = request.POST.get("mailId")
    try:
        email = models.Email.objects.get(email_id=emailId)
        email.pop_log = 0
        email.save()
        return JsonResponse({"message": "日志清除成功", "status": 200})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 后台主页数据
def AdminIndexInfo(request):
    try:
        smtpLogCnt = models.Email.objects.filter(smtp_log=1).count()
        popLogCnt = models.Email.objects.filter(pop_log=1).count()
        userCnt = models.User.objects.all().count()
        emailCnt = models.Email.objects.all().count()
        return JsonResponse({
            "message": "返回数据成功",
            "status": 200,
            "smtpLogCnt": smtpLogCnt,  # smtp日志数
            "popLogCnt": popLogCnt,    # pop日志数
            "userCnt": userCnt,        # 用户数
            "emailCnt": emailCnt})     # 邮件数

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 用户主页数据
def IndexInfo(request):
    userId = request.session.get('userId')
    try:
        userEmail = models.User.objects.get(user_id=userId).user_email
        rcvEmailCnt = models.Email.objects.filter(email_to=userEmail, rcver_del_flag=0).count()
        yetReadCnt = models.Email.objects.filter(email_to=userEmail, rcver_del_flag=0, rcver_fr_flag=0).count()
        sendEmailCnt = models.Email.objects.filter(email_from=userEmail, sender_del_flag=0).count()
        deletedEmailCnt = models.Email.objects.filter(Q(email_to=userEmail, rcver_del_flag=1) | Q(email_from=userEmail, sender_del_flag=1)).count()
        return JsonResponse({
            "message": "返回数据成功",
            "status": 200,
            "rcvEmailCnt": rcvEmailCnt,    # 收件数
            "yetReadCnt": yetReadCnt,      # 未读邮件数
            "sendEmailCnt": sendEmailCnt,  # 发件数
            "deletedEmailCnt": deletedEmailCnt  # 已删除数
        })

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 已删除列表
def DeletedMailList(request):
    userId = request.session.get('userId')
    try:
        userEmail = models.User.objects.get(user_id=userId).user_email
        infoList = []
        emails = models.Email.objects.filter(Q(email_to=userEmail, rcver_del_flag=1) | Q(email_from=userEmail, sender_del_flag=1))
        for email in emails:
            infoList.append({'emailId': email.email_id,
                             'emailFrom': email.email_from,
                             'emailTo': email.email_to,
                             'subject': email.email_subject,
                             'sendTime': email.send_time})  # 原收/发件时间

        return JsonResponse({
            "message": "返回数据成功",
            "status": 200,
            "infoList": infoList
        })

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


# 恢复已删除邮件
# 参数：mailId
def RecoverDeletedMail(request):
    emailId = request.POST.get("mailId")
    userId = request.session.get('userId')
    try:
        userEmail = models.User.objects.get(user_id=userId).user_email
        email = models.Email.objects.get(email_id=emailId)
        if email.email_to == userEmail:
            email.rcver_del_flag = 0
        else:
            email.sender_del_flag = 0
        email.save()
        return JsonResponse({"message": "邮件已恢复", "status": 200})

    except Exception as e:
        return JsonResponse({"message": "数据库出错", "status": 404})


