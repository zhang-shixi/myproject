"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import view
from sql import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',view.hello),
    url(r'^user/register',views.register),#用户注册
    url(r'^user/login',views.login),#用户登录
    url(r'^user/findpassword',views.findpassword),#找回密码
    url(r'^user/updata',views.updata),#修改信息
    url(r'^exchange/putquestion',views.put_question), #提交问题
    url(r'^exchange/putanswer',views.put_answer), #提交回答
    url(r'^exchange/dropquestion',views.drop_question), #删除问题
    url(r'^exchange/dropanswer',views.drop_answer), #删除回答
    url(r'^exchange/allquestion',views.all_question),#获取批量问题
    url(r'^exchange/addlike',views.add_like), #添加喜欢
    url(r'^exchange/deletelike',views.delete_like), #移除喜欢
    url(r'^my/myquestion',views.my_question), #获取我发布的问题
    url(r'^my/myanswer', views.my_answer),  # 获取我回答的问题
    url(r'^my/mylike', views.my_like),  # 获取我喜欢的问题
    url(r'^my/addsubject', views.add_subject), #添加课程
    url(r'^my/deletesubject', views.delete_subject), #删除课程
    url(r'^my/mysubject', views.my_subject),  #获取我添加的课程
    url(r'^information/allsubject',views.all_subject), #获取所有课程
]
