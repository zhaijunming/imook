from django.conf.urls import url
from django.views.generic import  TemplateView


from organization import views


urlpatterns = [
    #课程机构列表页
    url(r'^list/$',views.OrgListView.as_view(),name='org_list'),
    #userask表单提交
    url(r'^add_ask/$',views.AddUserAsk.as_view(),name='add_ask'),
    #所有课程机构列表
    url(r'^org_home/(?P<org_id>\d+)/$',views.OrgHomeView.as_view(), name='org_home'),
    #课程机构的课程
    url(r'org_course/(?P<org_id>\d+)$',views.OrgCourseView.as_view(),name='org_course'),
    #课程机构信息
    url(r'org_desc/(?P<org_id>\d+)$',views.OrgDescView.as_view(),name='org_desc'),
    #课程机构讲师
    url(r'org_teacher/(?P<org_id>\d+)$',views.OrgTeacherView.as_view(),name='org_teacher'),
    #添加收藏/取消收藏
    url(r'add_fav/$',views.AddFavView.as_view(),name='add_fav'),

    #列出所有讲师
    url(r'teacher/list/$' ,views.TeacherListView.as_view(),name='teacher_list',),

    #讲师详情页面
    url(r'teacher/(?P<teacher_id>\d+)$',views.TeacherDetailView.as_view(),name='teacher_detail'),
]