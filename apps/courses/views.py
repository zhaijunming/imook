from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.views.generic import View
from django.db.models import Q

from utils.mixin_utils import LoginRequiredMixin

from .models import *
from operation.models import *
import json
# Create your views here.


#课程列表
class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        #课程搜索
        search_keyword = request.GET.get('keywords','')
        print(search_keyword)
        if search_keyword:
            all_courses = all_courses.filter(Q(name__icontains=search_keyword)|Q(desc__icontains=search_keyword)|Q(detail__icontains=search_keyword))



        sort = request.GET.get('sort','')
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')



        paginator = Paginator(all_courses, 6)
        # 获取前端传过来的要访问的页面数,比如说去第一页,就传过来1
        page = request.GET.get('page')
        try:
            # 比如说第一页,就返回第一页的数据
            all_courses = paginator.page(page)
        except PageNotAnInteger:
            # 如果传过来的页面数不是整数,就返回第一页
            all_courses = paginator.page(1)
        except EmptyPage:
            # 如果传过来的页面数超出范围,就返回最有一夜
            all_courses = paginator.page(paginator.num_pages)


        return render(request,'course-list.html',{
            'all_courses':all_courses,
            'hot_courses':hot_courses,
            'sort':sort,
        })





#课程详情
class CourseDetailView(View):
    def get(self,request,course_id):
        #根据课程id获取课程
        course = Course.objects.get(id=int(course_id))

        #增加课程点击数
        course.click_nums += 1
        course.save()

        #获取章节数
        course_lesson_num = course.lesson_set.all().count()

        #获取学习此课程的用户数
        learn_users = course.usercourse_set.all()[:5]

        #获取该课程机构下的所有老师的数量
        teacher_nums = course.course_org.teacher_set.all().count()

        # 课程/机构收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request,'course-detail.html',{
            'course':course,
            'course_lesson_num':course_lesson_num,
            'learn_users':learn_users,
            'teacher_nums':teacher_nums,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })





###################点击课程开始学习跳转页面######################################3333



class CourseInfoView(LoginRequiredMixin,View):
    '''显示课程所有章节'''


    def get(self,request,course_id):

        course = Course.objects.get(id=int(course_id))
        #点击开始学习之后,学习人数+1
        course.students += 1
        course.save()
        #usercourse表中关联用户和课程
        #在usercourse表中查询用户和课程是否关联
        user_course = UserCourse.objects.filter(user=request.user,course=course)
        #如果没关联就加入关联
        if not user_course:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()



        #获取课程章节
        lessons  = course.lesson_set.all()

        #根据每个课程id获取数据该课程的资源
        all_resources = CourseResource.objects.filter(course=course)

        return render(request,'course-video.html',{
            'course':course,
            'lessons':lessons,
            'all_resources':all_resources,
        })



class CommetView(LoginRequiredMixin,View):
    '''显示课程所有评论'''
    def get(self,request,course_id):
        #取出此id的课程
        course = Course.objects.get(id=int(course_id))

        #获取属于此课程的章节
        lessons  = course.lesson_set.all()

        #根据课程id获取该课程的所有评论
        all_comments = CourseComments.objects.filter(course_id=int(course_id))

        # 根据每个课程id获取数据该课程的资源
        all_resources = CourseResource.objects.filter(course=course)

        return render(request,'course-comment.html',{
            'course':course,
            'lessons':lessons,
            'all_resources':all_resources,
            'all_comments':all_comments,
        })




class AddCommentView(LoginRequiredMixin,View):
    '''添加课程评论'''
    def post(self,request):
        ret = dict()
        if not request.user.is_authenticated():
            ret['status'] = 'fail'
            ret['msg'] = '用户未登录'
            return HttpResponse(json.dumps(ret), content_type='applicaiton/json')


        #获取前端传过来的课程id和评论内容
        course_id = request.POST.get('course_id',0)
        course_comment = request.POST.get('comments','')

        if course_id and course_comment:
            #实例化课程评论表
            comments = CourseComments()
            #保存课程id到课程评论表
            comments.course_id = course_id
            #保存用户id到课程评论表
            comments.user = request.user
            #保存评论内容到课程评论表
            comments.comments = course_comment
            comments.save()

            ret['status'] = 'success'
            ret['msg']  = '添加成功'
        else:
            ret['status'] = 'fail'
            ret['msg'] = u'添加失败'
        return  HttpResponse(json.dumps(ret),content_type='applicaiton/json')
































