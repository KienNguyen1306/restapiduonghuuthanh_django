
from rest_framework import viewsets,generics,status,permissions
from rest_framework.views import APIView
from .serializer import *
from .models import *
from .pagination import *

from rest_framework.decorators import action
from rest_framework.response import Response

from django.http import Http404


from django.conf import settings

from django.db.models import F

class CaterogyViewSet(viewsets.ViewSet,
                        generics.ListAPIView ):
    queryset = Category.objects.all()
    serializer_class = CaterogySerializer


class CousesViewSet(viewsets.ViewSet,
                        generics.ListAPIView):
    serializer_class = CousesSerializer
    pagination_class = PaginationClass

    def get_queryset(self):
        couses = Couses.objects.filter(active = True)

        q = self.request.query_params.get('q')
        if q is not None:
            couses =couses.filter(sub__icontains = q)
        
        cate_id = self.request.query_params.get('caterogy_id')
        if cate_id is not None:
            couses = couses.filter(caterogy_id=cate_id)
        
        return couses

    @action(methods=['get'],detail=True,url_path='lessons')
    def get_lesson(self,request,pk):
        couses = Couses.objects.get(pk=pk)
        lessons  = couses.lesson.filter(active = True)

        # lessons =self.get_object().lesson.filter(active = True)
        q =request.query_params.get('q')
        if q is not None:
            lessons = lessons.filter(sub__icontains = q)
        return Response(LessonSerializer(lessons,many=True).data,
            status=status.HTTP_200_OK)
    



class LessonViewser(viewsets.ViewSet,generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active = True)
    serializer_class = LessonDetailSerializer
    
    @action(methods=['post'],detail=True,url_path='tag')
    def add_tag(self,request,pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags =request.data.get('tags')
            if tags is not None:
                for tag in tags:
                    t , _ = Tag.objects.get_or_create(name=tag)
                    lesson.tags.add(t)

                lesson.save()

                return Response(self.serializer_class(lesson).data,status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_404_NOT_FOUND)



    def get_permissions(self):
        if self.action in ['add_coment','take_action','rate']:
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]


    @action(methods=['post'],detail=True,url_path='add-comment')
    def add_coment(self,request,pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content,
                        lesson=self.get_object(),
                        creator = request.user)
            return Response(CommentSerializer(c).data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['post'],detail=True,url_path='like')
    def take_action(self,request,pk):
        try:
            action_type = int(request.data['type'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action=Action.objects.create(type=action_type,
                                        creator=request.user,
                                        lesson=self.get_object())
            return Response(ActionSerializer(action).data,
                                    status=status.HTTP_200_OK)


    @action(methods=['post'],detail=True,url_path='rate')
    def rate(self,request,pk):
        try:
            rating = int(request.data['rate'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r=Rating.objects.create(rate=rating,
                                    creator=request.user,
                                    lesson=self.get_object())
            return Response(RateSerializer(r).data,status=status.HTTP_200_OK)


    @action(methods=['get'],detail=True,url_path='views')
    def inc_view(self,request,pk):
        v,created = LessonView.objects.get_or_create(lesson =self.get_object())
        v.views =F('views') + 1
        v.save()

        v.refresh_from_db()
        return Response(LessonViewsSerializer(v).data,status=status.HTTP_200_OK)



class UserViewSet(viewsets.ViewSet,generics.CreateAPIView):
    queryset = User.objects.filter(is_active = True)
    serializer_class = UserSerializer


    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]
   
   
    @action(methods=['get'],detail=False,url_path='current-user')
    def get_current_user(self,request):
        return Response(self.serializer_class(request.user).data,
            status=status.HTTP_200_OK)



class CommentViewset(viewsets.ViewSet,
                    generics.DestroyAPIView,
                    generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]



    def destroy(self,request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


    def partial_update(self,request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)




class AouthInffo(APIView):
    def get(self,request):
        return Response(settings.OAUTH2_INFO,status=status.HTTP_200_OK)