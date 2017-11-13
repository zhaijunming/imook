from django.db import models
from datetime import datetime
from organization.models import *
# Create your models here.
#这里有多个表,course(课程表),lesson(章节表),Video(视频表),课程和章节是一对多的关系,一个课程有多个章节,章节和视频也是一对多关系,一个章节有多个视频
#courseresource(资源下载表),和课程表是一对多关系,一个课程有多个文件可以下载

class Course(models.Model):
    '''课程'''
    course_org = models.ForeignKey(CourseOrg,verbose_name='所属课程机构',null=True,blank=True)
    teacher = models.ForeignKey(Teacher,verbose_name='所属课程讲师',null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name='课程名')
    desc = models.CharField(max_length=300,verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    choice_degree = (
        ('cj','初级'),
        ('zj','中级'),
        ('gj','高级'),
    )
    degree = models.CharField(choices=choice_degree,max_length=2,verbose_name='课程难度')
    learn_times = models.IntegerField(default=0,verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name='封面图')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否是轮播图')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    categort = models.CharField(default='后端',max_length=20,verbose_name='课程类别')
    youneed_know = models.CharField(default="",max_length=300,verbose_name='课程须知')
    teacher_tell = models.CharField(default="",max_length=300,verbose_name='老师告诉你能学到什么')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')


    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'

    def __str__(self):
        return self.name

class Lesson(models.Model):
    '''章节'''
    course = models.ForeignKey(Course,verbose_name='所属课程')
    name = models.CharField(max_length=100,verbose_name='章节名称')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = '章节'

    def __str__(self):
        return self.name



class Video(models.Model):
    '''视频'''
    lesson  = models.ForeignKey(Lesson,verbose_name='所属章节')
    name = models.CharField(max_length=100,verbose_name='视频名称')
    url = models.URLField(max_length=100,default='',verbose_name='章节链接')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = '视频'

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    '''资源下载'''
    course = models.ForeignKey(Course,verbose_name='所属课程')
    name = models.CharField(max_length=100,verbose_name='名称')
    #只是存储文件的url,文件是被放到目录里的,由django自动完成的
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name='资源文件',max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = '课程资源'

    def __str__(self):
        return self.name


