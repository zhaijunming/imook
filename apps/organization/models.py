from django.db import models

# Create your models here.
from  datetime import datetime


class CityDict(models.Model):
    '''城市'''
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = "城市"

    def __str__(self):
        return self.name



class CourseOrg(models.Model):
    '''机构'''
    name = models.CharField(max_length=50,verbose_name='机构名称')
    choice_category = (
        ('pxjg', '培训机构'),
        ('gx', '高校'),
        ('gr', '个人'),
    )
    category = models.CharField(default='pxjg',max_length=20,choices=choice_category)
    desc = models.TextField(verbose_name='机构描述')
    click_num = models.IntegerField(default=0,verbose_name='点击数')
    fav_num = models.IntegerField(default=0,verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m',verbose_name='logo')
    address = models.CharField(max_length=150,verbose_name='机构地址')
    city  = models.ForeignKey(CityDict,verbose_name='机构所在城市')
    student = models.IntegerField(default=0,verbose_name='学习人数')
    course_nums = models.IntegerField(default=0,verbose_name='课程数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = '课程机构'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    '''老师'''
    org = models.ForeignKey(CourseOrg,verbose_name='所属机构')
    name = models.CharField(max_length=50,verbose_name='教师姓名')
    work_years = models.IntegerField(default=0,verbose_name='工作年限')
    work_company = models.CharField(max_length=50,verbose_name='就职公司')
    work_position = models.CharField(max_length=50,verbose_name='公司职位')
    points = models.CharField(max_length=50,verbose_name='教学特点')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像',default='')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'

    def __str__(self):
        return self.name