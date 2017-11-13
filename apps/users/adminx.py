import xadmin
from xadmin import views
from .models import  *



class GlobalSetting(object):
    site_title = "幕学网后台管理系统"
    site_footer = '慕学在线网'
    menu_style = "accordion"


class EmailVerfyRevordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']





xadmin.site.register(EmailVerfyRecord,EmailVerfyRevordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)








