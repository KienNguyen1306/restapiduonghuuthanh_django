
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')



class Category(models.Model):
    # p = models.CharField(primary_key=True)
    name = models.CharField(max_length=100,null=True,unique=True)

    def __str__(self):
        return self.name
    

class ItemBase(models.Model):
    class Meta:
        abstract = True

    sub = models.CharField(max_length=200,null=True)
    image =models.ImageField(upload_to='courses/%Y/%m',default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.sub


class Couses(ItemBase):
    class Meta:
        unique_together = ('sub','category')
        ordering = ['-id']

    des = models.TextField(null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)



class Lesson(ItemBase):
    class Meta:
        unique_together = ('sub','couses')

    content =models.TextField()
    couses = models.ForeignKey(Couses,related_name="lesson",on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag',blank=True,null=True)

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    content = models.TextField()
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    

class ActionBase(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)


    class Meta:
        abstract = True


class Action(ActionBase):
    LIKE,HAHA,HEART=range(3)
    ACTIONS=[
        (LIKE,'like'),
        (HAHA,'haha'),
        (HEART,'heart')
    ]
    type = models.PositiveBigIntegerField(choices=ACTIONS,default=LIKE)
    

class Rating(ActionBase):
    rate = models.PositiveSmallIntegerField(default=0)




class LessonView(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    lesson = models.OneToOneField(Lesson,on_delete=models.CASCADE)
