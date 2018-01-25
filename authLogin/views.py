from django.shortcuts import render
from django.shortcuts import HttpResponse
from simplejson import dumps
import datetime
from hashlib import sha256

from authLogin import models
from authLogin.service.forms import LoginForm
from authLogin.service.forms import RegisterForm


def register(request):
    """ 用于注册功能的视图函数

    """

    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if not form.is_valid():  # 验证失败，返回错误信息
            data = {'form_errors': form.errors}
            return HttpResponse(dumps(data))

        form.cleaned_data['join_time'] = datetime.datetime.now()
        del form.cleaned_data['confirm_password']  # 组装创建记录所需字段信息

        avatar = request.FILES.get('avatar')  # 获取用户头像
        if avatar:
            form.cleaned_data['avatar'] = avatar

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        shaObj = sha256(username.encode(encoding='utf-8'))
        shaObj.update(password.encode(encoding='utf-8'))
        form.cleaned_data['password'] = shaObj.hexdigest()  # 对用户密码sha256加密

        models.UserInfo.objects.create(**form.cleaned_data)  # 创建用户

        data = {'success': True, "location_href": '/login/'}
        return HttpResponse(dumps(data))


def login(request):
    """ 用于登陆功能的视图函数

    """

    if request.method == 'GET':
        form = LoginForm(request=request)
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':                                  # 登陆验证开始
        form = LoginForm(request=request, data=request.POST)
        if not form.is_valid():                                     # 验证信息格式错误
            data = {'form_errors': form.errors}
            return HttpResponse(dumps(data))

        username = form.cleaned_data['username']
        raw_password = form.cleaned_data['password']
        shaObj = sha256(username.encode(encoding='utf-8'))
        shaObj.update(raw_password.encode(encoding='utf-8'))        # 将用户密码加密保存到数据库
        password = shaObj.hexdigest()

        user_queryset = models.UserInfo.objects.filter(username=username, password=password)
        if not user_queryset:                                        # 登陆失败
            form.add_error(field='password', error='用户名或密码错误')
            data = {'form_errors': form.errors}
            return HttpResponse(dumps(data))                         # 返回错误信息
        else:

            auto_login = request.POST.get('auto_login')
            # 登陆成功，初始化session数据
            request.session['username'] = username
            request.session['id'] = user_queryset[0].id
            if auto_login == '1':
                request.session.set_expiry(60 * 60 * 24 * 30)
            data = {'success': True}
            return HttpResponse(dumps(data))