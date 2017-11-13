from django.conf.urls import url
from django.views.generic import  TemplateView


from courses import views


urlpatterns = [
    #课程机构列表页
    url(r'^list/$',views.CourseListView.as_view(),name='course_list'),
    #课程详情
    url(r'^detail/(?P<course_id>\d+)/$', views.CourseDetailView.as_view(), name='course_detail'),
    #课程开始学习-->章节详情
    url(r'^info/(?P<course_id>\d+)/$', views.CourseInfoView.as_view(), name='course_info'),
    #课程开始学习-->评论显示
    url(r'^comment/(?P<course_id>\d+)/$', views.CommetView.as_view(), name='course_comment'),
    #课程评论提交
    url(r'^add_comment/$', views.AddCommentView.as_view(), name='add_comment'),


]