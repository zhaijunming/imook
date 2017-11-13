import xadmin
from xadmin import views


from .models import  *




class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']




class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num','fav_num','image','address','city','add_time']
    search_fields = ['name', 'desc', 'click_num','fav_num','image','address','city' ]
    list_filter = ['name', 'desc', 'click_num','fav_num','image','address','city','add_time']





class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years','work_company','work_position','points','click_num','fav_num','add_time']
    search_fields = ['org', 'name', 'work_years','work_company','work_position','points','click_num','fav_num',]
    list_filter = ['org__name', 'name', 'work_years','work_company','work_position','points','click_num','fav_num','add_time']

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)