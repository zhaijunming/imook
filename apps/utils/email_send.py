from random import Random
import string

from django.core.mail import send_mail

from users.models import EmailVerfyRecord
from MxOnline.settings import EMAIL_FROM


'''生成随机字符串'''
def random_str(random_length=16):
    code = ''
    # 26个大小写字母加数字
    chars = string.ascii_letters + str(string.digits)
    length = len(chars) - 1

    for i in range(random_length):
        code += chars[Random().randint(0, length)]
    return code



def send_register_email(email,send_type='register'):
    email_record = EmailVerfyRecord()
    #生成随机字符串
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body  = ""

    if send_type == 'register':
        email_title = "慕学在线网注册激活连接"
        email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = "慕学在线网密码重置链接"
        email_body = "请点击下面的链接重置密码:http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = "慕学在线网更改邮箱"
        email_body = "更改邮箱验证码为:{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass