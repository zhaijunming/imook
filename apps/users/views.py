from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from .models import UserProfile,EmailVerfyRecord,Banner
from operation.models import  *
from organization.models import *
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin #确保登录才能访问某些页面
import json

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            #Q方法的作用是或的意思,acc_login方法把username和password传过来,如果传过来的username是email,username就等于email,如果传过来的是username,username就等于username
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            #检测username和password是否匹配
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# 慕学在线网首页
class IndexView(View):
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })





# def acc_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             if user.is_active:
#                 login(request,user)
#                 return render(request,'index.html')
#             else:
#                 return render(request,'login.html',{'msg':'用户未激活'})
#         else:
#             return render(request, 'login.html',{'mgs':'用户名或密码错误'})
#     elif request.method == 'GET':
#         return render(request,'login.html')


class LogoutView(View):
    def get(self,request):
        logout(request)
        return  HttpResponseRedirect(reverse('index'))


'''登录'''
class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        login_form = LoginForm(request.POST)
        #如果form验证成功
        if login_form.is_valid():
            #获取前端数据的数据
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            #如果authenticate验证失败就会返回None,这个就会调用CustomBackend方法验证(重写了authenticate方法)
            user = authenticate(username=user_name, password=pass_word)
            #如果不是None,就是(authenticate)用户名密码验证成功
            if user is not None:
                #如果用户是激活状态
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            #验证失败
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        #验证失败
        else:
            #把form传给前端,因为form里包含错误信息(dict)
            return render(request,'login.html',{'login_form':login_form})


'''注册账户'''
class RegisterView(View):
    #显示注册页面
    def get(self,request):
        #把form传给前端,里边是验证码需要在前端显示
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    #接收提交的数据,进行逻辑判断
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            #去库里查询有没有这个邮箱,有就是已经注册过了
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已经存在'})
            #没有就是新用户,继续流程
            else:
                #获取前端填的表单,写进user库里
                pass_word = request.POST.get('password', '')
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.password = make_password(pass_word) #加密密码之后再存入库
                user_profile.save()


            send_register_email(user_name,'register')
            return  render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})#把register_form传给前端是因为 这里包含错误信息,需要在前端显示


'''激活账号'''
# 验证用户注册后，在邮件里点击注册链接
class ActiveUserView(View):
    def get(self,request,active_code):
        print(active_code)
        # 用户点击注册链接,类似于:http://127.0.0.1:8000/active/jdZFMyVHTZV7R2MC/,通过这个视图,接收到code字段:jdZFMyVHTZV7R2MC,去数据库里查这个code的记录(包括验证码,邮箱地址等),以code为条件去验证码的表里过滤出来这个code对应的邮箱
        all_record = EmailVerfyRecord.objects.filter(code=active_code)
        #判断是否查到数据
        if all_record:
            #查到之后,获取这个code的所有字段
            for recode in all_record:
                #获取这个code的邮箱地址
                email = recode.email
                #根据这个邮箱地址,去userProfile表里获取到这个邮箱地址的账号
                user  = UserProfile.objects.get(email=email)
                #把该账号的状态改为active
                user.is_active = True
                #保存
                user.save()
                return render(request,'login.html')
        else:
            return HttpResponse('faild,没有这个数据')

# 忘记密码页面
class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email, 'forget')
            return render(request,'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form': forget_form})

# 用户进入到重置密码页面
class ResetView(View):
    def get(self,request,active_code):
        # 以code为条件去数据库里查询,查到code对应的email,因为要知道用户给哪个email重置密码
        all_record = EmailVerfyRecord.objects.filter(code=active_code)
        # 如果查到数据
        if all_record:
            #循环这个对象
            for recode in all_record:
                # 获取email这个字段
                email = recode.email
                # 把email这个字段传给前端,在前端页面填写新的密码
                return render(request,'password_reset.html',{'email':email})
        # 如果没查到数据
        else:
            return render(request,'password_reset.html')


# 用户在重置密码页面提交新密码
class ModifyPwdView(View):
    def post(self,request):
        Modify_Form = ModifyPwdForm(request.POST)
        if Modify_Form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'msg':'密码输入不一致'})
            else:
                User = UserProfile.objects.get(email=email)
                User.password = make_password(pwd1)
                User.save()
                return render(request,'login.html')
        else:
            email = request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'Modify_Form':Modify_Form})




#个人中心页面-->信息显示
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html',{})
    def post(self,request):
        res = dict()
        userinfo = UserInfoForm(request.POST,instance=request.user)
        if userinfo.is_valid():
            userinfo.save()
            res['status']  = 'success'
        else:
            res = userinfo.errors
            print(json.dumps(res))
            # 假如address字段信息未填写,报错信息是这样的:"address": ["这个字段是必填项"]}
        return  HttpResponse(json.dumps(res),content_type='application/json')


#个人中心页面-->更改头像
class UploadImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        res = dict()
        if image_form.is_valid():
            image_form.save()
            res['status'] ='success'
            res['msg'] = '头像修改成功'
        else:
            res['status'] ='fail'
            res['msg'] = '头像修改失败'
        return HttpResponse(json.dumps(res),content_type='application/json')

#个人中心页面-->修改密码
class UpdatePwdView(LoginRequiredMixin,View):
    def post(self,request):
        modify_pwd = ModifyPwdForm(request.POST)
        res = dict()
        if modify_pwd.is_valid():
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                res['status'] = 'fail'
                res['msg'] = '两次密码输入不一致'
                return  HttpResponse(json.dumps(res),content_type='application/json')
            else:
                user = request.user
                user.password = make_password(password1)
                user.save()
                res['status'] = 'success'
                res['msg']  = '密码修改成功'
                return  HttpResponse(json.dumps(res),content_type='applicaiton/json')


        else:
            res = modify_pwd.errors
            return  HttpResponse(json.dumps(res),content_type='applicaiton/json')

#个人中心页面-->发送更改邮箱时的验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"邮箱已经存在"}',content_type='applicaiton/json')
        else:
            send_register_email(email,'update_email')
            return  HttpResponse('{"status":"success"}',content_type='applicaion/json')

#个人中心页面-->更改邮箱地址
class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email = request.POST.get('email','')
        code  = request.POST.get('code','')
        print('1')
        print(email,code)
        existing_record = EmailVerfyRecord.objects.filter(email=email,code=code,send_type='update_email')
        res = dict()
        if existing_record:
            user = request.user
            user.email = email
            user.save()
            res['status'] = 'success'
            res['msg'] = '邮箱修改成功'
        else:
            res['status'] = 'fail'
            res['msg'] = '验证码出错！'
        return HttpResponse(json.dumps(res), content_type='application/json')

#个人中心页面-->我的课程
class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses,
        })

#个人中心页面-->我的收藏-->我的收藏课程机构
class MyFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            fav_id = fav_org.fav_id
            org =  CourseOrg.objects.get(id=fav_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list,
        })


#个人中心页面-->我的收藏-->我收藏的授课讲师
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
        })


#个人中心页面-->我的收藏-->我收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
        })



# 全局 404 处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 全局 500 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response









