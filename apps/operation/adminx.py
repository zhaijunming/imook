import xadmin
from xadmin import views

from .models import  *




class userAskAdmin(object):
    list_display = ['name', 'mobile','course_name','add_time']
    search_fields = ['name', 'mobile','course_name']
    list_filter = ['name', 'mobile','course_name','add_time']


class CourseCommentsAdmin(object):
    '''课程评论'''
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


class UserFavoriteAdmin:
    '''用户收藏'''
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']



class UserMessageAdmin(object):
    '''用户消息'''
    list_display = ['user', 'message','has_read','add_time']
    search_fields = ['user', 'message','has_read']
    list_filter = ['user', 'message','has_read','add_time']



class UserCourseAdmin(object):
    '''用户课程'''
    list_display = ['user', 'course','add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course','add_time']



xadmin.site.register(userAsk,userAskAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)


