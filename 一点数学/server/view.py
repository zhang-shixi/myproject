from django.http import HttpResponse


def hello(request):
    return HttpResponse("服务器成功启动！")


