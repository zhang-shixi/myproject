from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.CharField(max_length=150, null=True)
    image = models.ImageField(default="../static/default/headimg.jpg", upload_to='../media/headimg') #头像
    background = models.ImageField(default="../static/default/background.jpg", upload_to='../media/background') #背景
    setting = models.CharField(max_length=400,blank=True) #用户自定义配置文件
    status = models.BooleanField(default=True) #账户状态
    def __str__(self):
        return self.name



class Question(models.Model):
    content = models.CharField(max_length=400)
    subject = models.CharField(max_length=150)
    point = models.CharField(max_length=150)
    picture = models.ImageField(default="../static/default/question.jpg", upload_to='../media/question')
    add_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="present_user")
    like = models.ManyToManyField(User, related_name="like_user",blank=True)


    def __str__(self):
        return self.content



class Answer(models.Model):
    content = models.CharField(max_length=400)
    add_date = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)


    def __str__(self):
        return self.content




class Subject(models.Model):
    name = models.CharField(max_length=150)
    add = models.ManyToManyField(User,blank=True,related_name="add_subject")


    def __str__(self):
        return self.name





