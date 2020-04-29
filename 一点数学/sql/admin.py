from django.contrib import admin
from sql.models import User,Question,Answer,Subject

# Register your models here.\
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','status')
    search_fields = ('name',)



class AnswerInline(admin.TabularInline):
    model = Answer



class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('content','subject','point','user','add_date',)
    search_fields = ('subject','point','user',)



class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content','user','add_date','question')
    search_fields = ('user',)




admin.site.register(User,UserAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Subject)