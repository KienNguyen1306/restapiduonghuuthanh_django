
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import *

class CaterogySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CousesSerializer(ModelSerializer):
    image = SerializerMethodField()
    def get_image(self,couses):
        request = self.context['request']
        name = couses.image.name
        if name.startswith('static/'):
            path = '/%s' %name
        else:
            path = '/static/%s'%name
        return request.build_absolute_uri(path)
    

    class Meta:
        model = Couses
        fields = ['id','sub','create_date','image','category']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
            


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id','sub','image','create_date','update_date','couses']


class LessonDetailSerializer(LessonSerializer):
    tags = TagSerializer(many = True)
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content','tags']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password','date_joined']

        # ============= chỉ để tạo password không hieent thị password =========
        extra_kwargs = {
            'password':{'write_only':'True'}
        }
    
    # ===============ghi đè (băm mk)=================
    def create(self, validated_data):
        user = User(**validated_data)
        # user.first_name = validated_data['first_name']
        # ...
        # user.set_password(validated_data['password'])

        user.set_password(validated_data['password'])
        user.save()

        return user
    

class CommentSerializer(ModelSerializer):
    class Meta:     
        model = Comment
        fields = ['id','content','create_date','update_date']



class ActionSerializer(ModelSerializer):
    class Meta:     
        model = Action
        fields = ['id','type','create_date']


class RateSerializer(ModelSerializer):
    class Meta:     
        model = Rating
        fields = ['id','rate','create_date']


class LessonViewsSerializer(ModelSerializer):
    class Meta:     
        model = LessonView
        fields = ['id','views','lesson']


