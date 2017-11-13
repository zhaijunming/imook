import xadmin
from xadmin import views
from organization.models import *

from .models import  *

class CourseAdmin(object):
    list_display = ['name','course_org','teacher','desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name','course_org', 'teacher','desc', 'detail', 'degree','students','fav_nums','image','click_nums']
    list_filter = ['course_org__name','name','teacher', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums','add_time']



class LessonAdmin(object):
    list_display = ['name','course', 'add_time']
    search_fields = ['name','course']
    #由于lesson和course是一对多关系,一个课程有多个章节,这里的course是course 的外键,想要根据课程名称过滤章节的话,需要指定course中的一个字段,比如说name,就是根据课程名过滤属于这个课程名称的所有章节
    list_filter = ['course__name', 'name','add_time']


class VideoAdmin(object):
    list_display  = ['name','lesson','add_time']
    search_fields = ['name','lesson',]
    list_filter   = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['name','course', 'download','add_time']
    search_fields = ['name','course', 'download']
    list_filter = ['course__name', 'name','download','add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)































