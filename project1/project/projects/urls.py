from django.urls import path,include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register("api/caterogy",views.CaterogyViewSet,"caterogy")
router.register('api/couses',views.CousesViewSet,'couses')
router.register('api/lesson',views.LessonViewser,'lesson')
router.register('api/user',views.UserViewSet,'user')
router.register('api/comments',views.CommentViewset,'comment')

urlpatterns = [
     path('',include(router.urls)),
     path('outh2_info/',views.AouthInffo.as_view())
]


