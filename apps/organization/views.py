from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage


from .models import CityDict,CourseOrg,Teacher
from operation.models import *
from .forms import *

import json
# Create your views here.





class OrgListView(View):
    '''显示所有课程机构并按条件筛选'''
    def get(self,request):


        '''说明:
        按一个条件查找:
            请求地址:http://127.0.0.1:8000/org/list/?city=1
            先获取所有课程机构
            如果前端通过城市筛选课程机构的话,点击城市的时候会发送一个get请求,把城市id传过来
            这里根据城市id过滤出对应的课程机构传给前端进行展示
        按两个条件查找:
            请求地址:http://127.0.0.1:8000/org/list/?city=1&ct=pxjg
            1.先获取所有课程机构
            2.前端先点击课程机构类型筛选的话,点击课程机构类型的时候会发送一个get请求,把类型和城市id传过来(城市id这个时候为空,因为没点击城市)
            3.这里根据类型过滤出对应的课程机构传给前端展示,并把机构类型传给前端
            4.前端再点击城市进行筛选的话,点击城市的时候会发送一个get请求,把城市id和机构类型(这里机构类型是上一步根据机构类型筛选的时候传给前端的)传过来
            5.这里先获取所有课程机构,然后再根据城市id筛选课程机构记录结果,在根据机构类型继续筛选课程机构,把结果传给前端进行展示
        按三个条件查找:
            请求地址:http://127.0.0.1:8000/org/list/?sort=students&ct=pxjg&city=1
            1.先获取所有课程机构
            2.前端先点击课程机构类型筛选的话,点击课程机构类型的时候会发送一个get请求,把类型和城市id传过来(城市id这个时候为空,因为没点击城市)
            3.这里根据类型过滤出对应的课程机构传给前端展示,并把机构类型传给前端
            4.前端再点击城市进行筛选的话,点击城市的时候会发送一个get请求,把城市id和机构类型(这里机构类型是上一步根据机构类型筛选的时候传给前端的)传过来
            5.这里先先获取所有课程机构,然后再根据城市id筛选课程机构记录结果,在根据机构类型继续筛选课程机构,把结果传给前端进行展示,并把城市id传给前端
            6.前端再点击学习人数进行筛选的话,点击学习人数会发送一个get请求,把城市id和机构类型和以学习人数为条件传过来
            7.这里在按条件一层一层筛选,并传给前端展示
        '''

        '''所有课程机构'''
        #如果没指定过滤条件就显示所有课程机构
        all_orgs = CourseOrg.objects.all()

        '''所有城市'''
        all_citys = CityDict.objects.all()

        '''统计出所有课程机构中点击数排名前三的'''
        hot_orgs =  all_orgs.order_by('-click_num')[:3]

        '''按城市筛选课程机构'''
        #获取前端通过get请求传过来的城市id
        city_id = request.GET.get('city','')
        if city_id:
            #以城市id为条件去数据库里获取数据
            all_orgs = all_orgs.filter(city_id=int(city_id))

        '''按课程机构类型筛选课程机构'''
        #获取前端通过get请求传过来的课程机构类型
        category = request.GET.get('ct','')
        if category:
            #以课程机构类型为条件去数据库里获取数据
            all_orgs = all_orgs.filter(category=category)



        search_keyword = request.GET.get('keywords','')
        if search_keyword:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keyword)|
                                       Q(desc__icontains=search_keyword))

        '''课程机构排序'''
        sort = request.GET.get('sort','')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-student')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')



        '''对课程机构进行分页'''
        paginator = Paginator(all_orgs, 3)
        page = request.GET.get('page')
        org_nums = all_orgs.count()
        try:
            orgs = paginator.page(page)
        except PageNotAnInteger:
            orgs = paginator.page(1)
        except EmptyPage:
            orgs = paginator.page(paginator.num_pages)





        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })


class AddUserAsk(View):
    '''用户提交问答'''
    def post(self,request):
        ret = {'status':False,'msg':None}
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            ret['status'] = True
            return HttpResponse(json.dumps(ret),content_type="application/json")
        else:
            ret['status'] = False
            ret['msg'] = '请确认信息填写正确'

            return HttpResponse(json.dumps(ret),content_type="application/json")







class OrgHomeView(View):
    '''某个课程机构详情页面'''
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))      #获取id=org_id的机构
        #用户点击该课程机构,点击数+1
        course_org.click_num += 1
        course_org.save()
        all_courses = course_org.course_set.all()[:4]           #获取这个机构下的所有课程
        all_teacher = course_org.teacher_set.all()[:1]          #获取这个机构下所有的老师

        current_page = 'home'

        # 初始化判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })





class OrgCourseView(View):
    '''某个课程机构详情页-->所有课程'''
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        paginator = Paginator(all_courses, 3)
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

        current_page = 'course'

        # 初始化判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-course.html',{
            'course_org':course_org,
            'all_courses':all_courses,
            'current_page': current_page,
            'has_fav': has_fav,

        })


class OrgDescView(View):
    '''某个课程机构详情页面-->机构介绍'''
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))      #获取id=org_id的机构

        current_page = 'desc'

        # 初始化判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })






class OrgTeacherView(View):
    '''某个机构详情页面--->所有讲师'''
    def get(self,request,org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        paginator = Paginator(all_teachers, 3)
        page = request.GET.get('page')

        try:
            # 比如说第一页,就返回第一页的数据
            all_teachers = paginator.page(page)
        except PageNotAnInteger:
            # 如果传过来的页面数不是整数,就返回第一页
            all_teachers = paginator.page(1)
        except EmptyPage:
            # 如果传过来的页面数超出范围,就返回最有一夜
            all_teachers = paginator.page(paginator.num_pages)

        current_page = 'teacher'

        # 初始化判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-teachers.html',{
            'course_org':course_org,
            'all_teachers':all_teachers,
            'current_page': current_page,
            'has_fav':has_fav,

        })


class AddFavView(View):
    '''用户收藏课程机构'''
    def post(self,request):
        fav_id = request.POST.get('fav_id','')
        fav_type = request.POST.get('fav_type','')
        ret = dict()
        if not request.user.is_authenticated():
            ret['status'] = 'fail'
            ret['msg'] = '用户未登录'
        else:
            user_fav = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
            if user_fav:
                user_fav.delete()
                #用户取消收藏的时候,就把点击数-1,比如用户取消收藏课程,那就把该课程点击数-1
                if int(fav_type) == 1:
                    course = Course.objects.get(int(fav_id))
                    course.fav_nums -=1
                    if course.fav_nums < 0: #防止负数出现
                        course.fav_nums = 0
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_num -= 1
                    if course_org.fav_nums < 0:
                        course_org.fav_nums = 0
                    course_org.save()
                elif int(fav_type)  == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num -=1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()

                ret['status'] = 'success'
                ret['msg'] = '收藏'
            else:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                # 用户收藏的时候,就把点击数+1,比如用户收藏课程,那就把该课程点击数+1
                if int(fav_type) == 1:
                    course = Course.objects.get(int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_num += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num += 1
                    teacher.save()

                ret['status'] = 'success'
                ret['msg'] = '已收藏'
        return HttpResponse(json.dumps(ret),content_type='applicaiton/json')




class TeacherListView(View):
    '''所有讲师列表'''
    def get(self,request):
        all_teachers = Teacher.objects.all()
        sorted_teachers = all_teachers.order_by('-click_num')[:3]


        search_keyword = request.GET.get('keywords','')
        if search_keyword:
            all_teachers.filter(Q(name__icontains=search_keyword))

        sort = request.GET.get('sort','')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_num')

        paginator = Paginator(all_teachers, 3)
        # 获取前端传过来的要访问的页面数,比如说去第一页,就传过来1
        page = request.GET.get('page')
        try:
            # 比如说第一页,就返回第一页的数据
            all_teachers = paginator.page(page)
        except PageNotAnInteger:
            # 如果传过来的页面数不是整数,就返回第一页
            all_teachers = paginator.page(1)
        except EmptyPage:
            # 如果传过来的页面数超出范围,就返回最有一夜
            all_teachers = paginator.page(paginator.num_pages)




        return render(request,'teachers-list.html',{
            'all_teachers':all_teachers,
            'sorted_teachers':sorted_teachers,
            'sort':sort
        })


class TeacherDetailView(View):
    '''讲师详情页面'''
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        #点击讲师详情之后该讲师点击数+1
        teacher.click_num += 1
        teacher.save()
        #取数属于该讲师的所有课程
        all_courses = teacher.course_set.all()
        sorted_teachers = Teacher.objects.order_by('-click_num')

        # 课程/机构收藏
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
                print(has_fav_teacher)
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True
                print(has_fav_org)




        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teachers':sorted_teachers,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
        })






















