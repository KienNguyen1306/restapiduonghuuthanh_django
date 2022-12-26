
from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets,permissions,generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .models import *
from .serializer import CousesSerializer,LessonSerializer,UserSerializer,JoinSerializer


class UserViewSet(viewsets.ViewSet,
                generics.ListAPIView,
                generics.DestroyAPIView,
                generics.CreateAPIView,
                generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # ============ upload file ============
    parser_classes = [MultiPartParser,]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]   
        return [permissions.AllowAny()]


class CousesViewSet(viewsets.ModelViewSet):
    queryset = Couses.objects.filter(active = True)
    serializer_class = CousesSerializer
    # permission_classes =[permissions.IsAuthenticated]

# ============= kkhong dùng drf_yasg ================
    # swagger_schema = None

# ================ dăng mnhaapj mới đi=ược xem ==================
    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]     
    #     return [permissions.IsAuthenticated()]
    
class LessonViewser(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializer


    # cung cap an api khoas hoc?
    @action(methods=['post'],detail=True,url_path='hide-lesson',url_name='hide-lesson')
    # /lesson/{pk}/hide-lesson
    def hide_lesson(self,request,pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False  
            l.save() 
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=LessonSerializer(l,context= {'request':request}).data,status=status.HTTP_200_OK)



    
# class JoinViewser(viewsets.ModelViewSet):
#     queryset = Couses.objects.filter(category__id = Category['id'])
#     serializer_class = JoinSerializer
