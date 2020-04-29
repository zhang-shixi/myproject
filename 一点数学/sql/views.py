from django.http import HttpResponse
from sql.models import User,Question,Answer,Subject
from django.core.mail import send_mail
import json
import socket
#
#
#
def send(id): #提醒用户刷新
    try:
        ip = on_line_user[str(id)][0]
        port = on_line_user[str(id)][1]
        sk = socket.socket()
        try:
            sk.connect((ip, port))
            data = "更新数据"
            sk.sendall(data)
        except:
            on_line_user.pop(str(id))
        finally:
            sk.close()
    except:
        return 0


def register(request):  #注册函数
    name = request.GET.get('name')
    password = request.GET.get('password')
    email = request.GET.get('email')
    try:
        result = User.objects.get(name=name)
        return HttpResponse("用户名已存在")
    except:
        try:
            result = User.objects.get(email=email)
            return HttpResponse("邮箱已存在")
        except:
            use = User(name=name, password=password,email = email)
            use.save()
            return HttpResponse(name + "注册成功")


def login(request):  #登录函数
    try:
        name = request.GET.get('name')
        password = request.GET.get('password')
        result= User.objects.get(name=name).password
        if result==password:
            request.session['username'] = name
            request.session['is_login'] = True
            inf = {}
            inf['id'] = str(User.objects.get(name=name).id)
            inf['image'] = str(User.objects.get(name=name).image)
            inf['background'] = str(User.objects.get(name=name).background)
            inf['setting'] = str(User.objects.get(name=name).setting)
            return HttpResponse(json.dumps(inf), content_type="application/json")
        else :
            return HttpResponse("密码错误")
    except:
        return HttpResponse("用户名错误")



def updata(request):  #修改信息
    if request.method == 'POST':
        id = request.POST.get('id')
        newname = request.POST.get('newname')
        newpassword = request.POST.get('newpassword')
        newemail = request.POST.get('email')
        newimage = request.FILES.get('image')
        newbackground = request.FILES.get('background')
        newsetting = request.POST.get('newsetting')
        try:
            result = User.objects.get(id=id)
            if newname != '':
                result.name = newname
            if newpassword != '':
                result.password = newpassword
            if newemail != '':
                result.email = newemail
            if newimage != '':
                result.image = newimage
            if newbackground != '':
                result.background = newbackground
            if newsetting != '':
                result.setting = newsetting
            result.save()
            return HttpResponse("信息修改成功")
        except:
            return HttpResponse("用户名不存在")


def findpassword(request): #找回密码
    email = request.GET.get('email')
    try:
        result = User.objects.get(email=email)
        message = '您正在找回帐号，'+str(email)+'对应的用户名为 '+str(result.name)+' ,密码为 '+str(result.password)+' ,如不是本人操作请忽略。'
        # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
        send_mail('一点数学帐号找回', message, '1096244328@qq.com',[email], fail_silently=False)
        return HttpResponse("发送成功请在邮箱查看账户信息")
    except:
        return HttpResponse("邮箱不存在")


def put_question(request): #提交问题
    if request.method == 'POST':
        content = request.POST.get('content')
        subject = request.POST.get('subject')
        point = request.POST.get('point')
        picture = request.FILES.get('picture')
        user_id = request.POST.get('user_id')
        request= Question(content=content,subject=subject,point=point,picture=picture,user_id=user_id)
        request.save()
        return HttpResponse(str(request.id))


def drop_question(request): #删除问题
    id = request.GET.get('id')
    result = Question.objects.get(id=id).delete()
    return HttpResponse('删除成功')


def put_answer(request): #提交回答
    if request.method == 'POST':
        content = request.POST.get('content')
        user_id = request.POST.get('user_id')
        question_id = request.POST.get('question_id')
        question_user_id = Question.objects.get(id=question_id)
        send(question_user_id)
        answer= Answer(content=content,user_id=user_id,question_id=question_id)
        answer.save()
        return HttpResponse(str(answer.id))



def drop_answer(request): #删除回答
    id = request.GET.get('id')
    result = Answer.objects.get(id=id).delete()
    return HttpResponse('删除成功')


#获取的题目为json格式 题目id对应题目详情 题目详情为列表 各字段分别为发布人，科目，知识点，题目内容，题目图片，发布时间，关注数，回答
# 回答也为json格式，回答id对应回答详情 回答详情各字段为回答人，回答内容，回答时间


def all_question(request): #获取问题 point为空全部获取不为空关键字检索
    start = int(request.GET.get('start'))
    end = int(request.GET.get('end'))
    point = request.GET.get('point')
    if point=="":
        question = Question.objects.all().order_by('-add_date')
    else:
        question = Question.objects.filter(point=point).order_by('-add_date')
    max = len(question)
    result = {}
    if start>max:
        return HttpResponse("没有更多数据了")
    if max>=start and max<=end:
        for i in question[start:]:
            answer_result = {}
            answer = i.answer_set.all().order_by('add_date')
            for j in answer:
                answer_result[j.id] = [str(j.user),str(j.content),str(j.add_date)]
            result[i.id] = [str(i.user),str(i.subject),str(i.point),str(i.content),str(i.picture),str(i.add_date),str(i.like.all().count()),answer_result]

        return HttpResponse(json.dumps(result), content_type="application/json")
    if max>end:
        for i in question[start:end]:
            answer_result = {}
            answer = i.answer_set.all().order_by('add_date')
            for j in answer:
                answer_result[j.id] = [str(j.user),str(j.content),str(j.add_date)]
            result[i.id] = [str(i.user),str(i.subject),str(i.point),str(i.content),str(i.picture),str(i.add_date),str(i.like.all().count()),answer_result]

        return HttpResponse(json.dumps(result), content_type="application/json")


def add_like(request): #添加喜欢
    user_id = request.GET.get('user_id')
    question_id = request.GET.get('question_id')
    result = Question.objects.get(id=question_id)
    result.like.add(user_id)
    return HttpResponse("添加喜欢成功")


def delete_like(request): #移除喜欢
    user_id = request.GET.get('user_id')
    question_id = request.GET.get('question_id')
    user = User.objects.get(id=user_id)
    question = Question.objects.get(id=question_id)
    question.like.remove(user)
    return HttpResponse("移除喜欢课程成功")


def my_question(request): #获取我发布的题目
    user_id = request.GET.get('user_id')
    question = Question.objects.filter(user_id=user_id).order_by('-add_date')
    result = {}
    for i in question:
        answer_result = {}
        answer = i.answer_set.all().order_by('add_date')
        for j in answer:
            answer_result[j.id] = [str(j.user), str(j.content), str(j.add_date)]
        result[i.id] = [str(i.user), str(i.subject), str(i.point), str(i.content), str(i.picture), str(i.add_date),
                        str(i.like.all().count()), answer_result]
    return HttpResponse(json.dumps(result), content_type="application/json")


def my_answer(request): #获取我回答的题目
    user_id = request.GET.get('user_id')
    answer = Answer.objects.filter(user_id=user_id)
    result = {}
    for n in answer:
        question = Question.objects.get(id=n.question_id)
        answer_result = {}
        answer = question.answer_set.all().order_by('add_date')
        for j in answer:
            answer_result[j.id] = [str(j.user), str(j.content), str(j.add_date)]
        result[question.id] = [str(question.user),str(question.subject),str(question.point),str(question.content),
                               str(question.picture),str(question.add_date),str(question.like.all().count()),answer_result]
    return HttpResponse(json.dumps(result), content_type="application/json")



def my_like(request):#获取我喜欢的题目
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    question = user.like_user.all()
    result = {}
    for i in question:
        answer_result = {}
        answer = i.answer_set.all().order_by('add_date')
        for j in answer:
            answer_result[j.id] = [str(j.user), str(j.content), str(j.add_date)]
        result[i.id] = [str(i.user), str(i.subject), str(i.point), str(i.content), str(i.picture), str(i.add_date),
                        str(i.like.all().count()), answer_result]
    return HttpResponse(json.dumps(result), content_type="application/json")


def add_subject(request): #添加课程
    user_id = request.GET.get('user_id')
    subject_id = request.GET.get('subject_id')
    result = Subject.objects.get(id=subject_id)
    result.add.add(user_id)
    return HttpResponse("添加课程成功")


def delete_subject(request): #删除课程
    user_id = request.GET.get('user_id')
    subject_id = request.GET.get('subject_id')
    user = User.objects.get(id=user_id)
    subject = Subject.objects.get(id=subject_id)
    subject.add.remove(user)
    return HttpResponse("删除课程成功")


def my_subject(request): #获取我添加的课程
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    subject = user.add_subject.all()
    result = {}
    for i in subject:
        result[i.id] = i.name
    return HttpResponse(json.dumps(result), content_type="application/json")


def all_subject(request):#获取所有课程
    result = Subject.objects.all()
    subject = {}
    for i in result:
        subject[i.id] = i.name
    return HttpResponse(json.dumps(subject), content_type="application/json")


















