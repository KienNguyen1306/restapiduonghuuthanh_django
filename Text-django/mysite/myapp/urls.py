from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('api/couses',views.CousesViewSet)
router.register('api/lesson',views.LessonViewser)
router.register('api/user',views.UserViewSet)
router.register('api/joni',views.JoinViewser)



#/couses/ -get
#/couses/ -post
#/couses/{couses_id} -get
#/couses/{couses_id} -put
#/couses/{couses_id} -delete

urlpatterns = [
    path('',include(router.urls)),
]


