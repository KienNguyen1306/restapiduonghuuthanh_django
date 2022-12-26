from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category,Couses,Lesson
# Register your models here.

class LessonAdmin(admin.ModelAdmin):
    list_display = ['id','sub','create_date','active','content','couses']
    search_fields = ['sub','create_date','couses__des']
    list_filter =['sub','couses__des']
    readonly_fields = ['avatar']

    def avatar(self,lesson):
        return mark_safe("<img src ='/static/{img_url}' alt='loi' width = '100px'/>".format(img_url = lesson.image.name))

    class Media:
        css ={
            'all':('/static/css/main.css',)
        }

admin.site.register(Category)
admin.site.register(Couses)
admin.site.register(Lesson,LessonAdmin)

