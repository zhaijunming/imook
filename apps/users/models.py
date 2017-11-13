from django.db import models
#引用内置的user模型
from django.contrib.auth.models import  AbstractUser
from datetime import datetime
# Create your models here.

#集成内置的user模型,并添加新的字段
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='')
    birday = models.DateField(null=True,blank=True,verbose_name='生日')
    choice_gender = (
        ("male","男"),
        ("female","女"),
    )
    gender = models.CharField(choices=choice_gender,default='female',max_length=6,verbose_name='性别')
    address = models.CharField(max_length=100,default='',verbose_name='地址')
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name='手机号')
    image = models.ImageField(upload_to='image/%Y/%m',default='image/default.png',max_length=100)


    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"


    def __str__(self):
        return self.username





class EmailVerfyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name='验证码')
    email = models.EmailField(max_length=50,verbose_name='邮箱')
    choice_send_type = (
        ('register','注册'),
        ('forget','找回密码'),
        ('update_email','更改邮箱'),
    )
    send_type = models.CharField(choices=choice_send_type,max_length=30,verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name='验证码发送时间')

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = "邮箱验证码"

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)



class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    #数据库只记录图片的地址
    image = models.ImageField(upload_to='banner/%Y%m',verbose_name='轮播图',max_length=100)
    #点击图片跳转到某个url,这个字段记录的是这个
    url = models.URLField(max_length=200,verbose_name='访问地址')
    #按大小顺序排序,比如1就是第一个,想把某个图片靠前显示就把这个字段调低
    index = models.IntegerField(default=100,verbose_name='顺序')
    #添加时间
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'



