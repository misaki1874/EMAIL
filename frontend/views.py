import pymysql
from django.http import JsonResponse
from django.shortcuts import render
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

def Login(request):
    return render(request,'Login.html')

# 用户认证
def user_identified(request):
    email = request.POST.get('email',None)
    password = request.POST.get('password',None)
    con = connectdb()
    cursor = con.cursor()
    sql = "SELECT user_code FROM user where user_email = '%s'"
    data = (email,)
    cursor.execute(sql%data)
    try:
        result = cursor.fetchone()
        code = result[0]
    except IndexError:  # 无记录 不存在该用户
        return 0
    cursor.close()
    con.close()
    # 密码验证
    if code == password:
        return JsonResponse({"message": "登陆成功"})
    else:
        return JsonResponse({"message": "邮箱或密码输入错误"})


# 注册
def SignUp(request):
    return render(request,'SignUp.html')

def Index(request):
    return render(request,'Index.html')

def GET_test(request):
    # 渲染这个页面 并返回到前端
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