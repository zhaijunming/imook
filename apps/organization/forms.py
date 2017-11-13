from django import forms
from operation.models import userAsk

import re

class UserAskForm(forms.ModelForm):
    class Meta:
        model = userAsk
        fields = ['name','mobile','course_name']

    def clean_mobile(self): #自定义mobile字段的验证,必须得这么写(定义name字段就是clean_name)
        #获取mobile字段内容
        mobile = self.cleaned_data['mobile']
        #定义验证规则
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        #把获取到的mobile字段进行验证
        #如果验证通过
        if p.match(mobile):
            # 这里还能返回外键
            return mobile
        #如果验证失败,这个错误信息可以通过.errors获取
        else:
            raise forms.ValidationError('mobile error', code='mobile_inval')
