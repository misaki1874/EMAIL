from django.shortcuts import render
from .models import User
# Create your views here.

def Login(request):
    return render(request,'Login.html')

def SignUp(request):
    return render(request,'SignUp.html')

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