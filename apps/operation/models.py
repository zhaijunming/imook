from datetime import datetime

from django.db import models

from courses.models import Course
from users.models import UserProfile


class userAsk(models.Model):
    '''用户咨询,页面中间部分  我要学习 表单提交'''
    name = models.CharField(max_length=20,verbose_name='姓名')
    mobile = models.CharField(max_length=11,verbose_name='手机')
    course_name = models.CharField(max_length=50,verbose_name='课程名称')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = '用户咨询'


class  CourseComments(models.Model):
    '''课程评论
        这个表就是
        某个用户对某个课程有某些评论
        user是外键,为了把userProfile表和coursecomments表关联起来'''
    user = models.ForeignKey(UserProfile,verbose_name='用户')
    course = models.ForeignKey(Course,verbose_name='课程')
    comments = models.CharField(max_length=200,verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')


    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = '课程评论'


class UserFavorite(models.Model):
    '''用户收藏'''
    user = models.ForeignKey(UserProfile,verbose_name='用户')
    #这个id是课程机构或者课程的id,比如课程机构的id是1,这里就是1(通过course_org.id获取)
    fav_id = models.IntegerField(default=0,verbose_name='数据ID')
    choice_fav_type = (
        (1,'课程'),
        (2,'课程机构'),
        (3, "讲师"),
    )
    fav_type = models.IntegerField(choices=choice_fav_type,verbose_name='收藏类型',default=1)
    add_time =  models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = '用户收藏'



class UserMessage(models.Model):
    '''用户消息'''
    #这里为用户的id
    user = models.IntegerField(default=0,verbose_name='接收用户')
    message = models.CharField(max_length=500,verbose_name='消息内容')
    has_read = models.BooleanField(default=False,verbose_name='是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = '用户消息'





class UserCourse(models.Model):
    '''用户的课程'''
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural =  "用户课程"






















