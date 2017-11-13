from django.conf.urls import url
from django.views.generic import  TemplateView


from users import views


urlpatterns = [
    #个人信息页面
    url(r'^info/$',views.UserInfoView.as_view(),name='user_info'),
    #修改头像
    url(r'^image/upload/$',views.UploadImageView.as_view(),name='upload_image'),
    #修改密码
    url(r'^update/pwd/$',views.UpdatePwdView.as_view(),name='update_pwd'),
    #修改个人邮箱时发送验证码
    url(r'^sendemail_code/$',views.SendEmailCodeView.as_view(),name='sendemail_code'),
    #修改个人邮箱
    url(r'^update_email/$',views.UpdateEmailView.as_view(),name='update_email'),
    #个人中心页面-->我的课程
    url(r'^mycourse/$',views.MyCourseView.as_view(),name='mycourse'),
    #个人中心页面我的收藏-->我收藏的课程机构
    url(r'^myfav_org/$',views.MyFavOrgView.as_view(),name='myfav_org'),
#个人中心页面我的收藏-->我收藏的讲师
    url(r'^myfav_teacher/$',views.MyFavTeacherView.as_view(),name='myfav_teacher'),
#个人中心页面我的收藏-->我收藏的课程
    url(r'^myfav_course/$',views.MyFavCourseView.as_view(),name='myfav_course'),
]