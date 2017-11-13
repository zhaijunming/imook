"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import  TemplateView
from users import views
import xadmin

from django.views.static import serve
from .settings import MEDIA_ROOT






urlpatterns = [
    # 后台
    url(r'^admin/', xadmin.site.urls),
    # 验证码
    url(r'^captcha/', include('captcha.urls')),
    # 主页
    url('^$',views.IndexView.as_view(),name='index'),
    # 登录
    url('^login/$',views.LoginView.as_view(),name='login'),
    #登出
    url('^logout/$',views.LogoutView.as_view(),name='logout'),
    # 注册
    url('^register/$',views.RegisterView.as_view(),name='register'),
    # 验证用户注册后，在邮件里点击注册链接
    url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name='user_active'),
    #忘记密码页面
    url('^forget/$',views.ForgetPwdView.as_view(),name='forget_pwd'),
    # 用户在邮件里点击重置密码链接
    url(r'^reset/(?P<active_code>.*)/$', views.ResetView.as_view(), name='reset_pwd'),
    # 重置密码表单 POST 请求
    url('^motify/$',views.ModifyPwdView.as_view(),name='modify_pwd'),

    #课程机构页面url配置(讲师)
    url('^org/',include('organization.urls',namespace='org')),
    #课程页面url配置
    url('^course/',include('courses.urls',namespace='course')),
    #用户人中心url
    url('^users/',include('users.urls',namespace='users')),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    #配置静态文件的访问处理函数
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),


]
# 全局 404 页面配置（django 会自动调用这个变量）
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'