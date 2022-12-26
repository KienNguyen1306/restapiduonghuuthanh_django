
from rest_framework.serializers import ModelSerializer

from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','avatar','password']
        
        # ============= chỉ để tạo password không hieent thị password =========
        extra_kwargs = {
            'password':{'write_only':'true'}
        }


# ===============ghi đè (băm mk)=================
    def create(self, validated_data):
        user = User(**validated_data)
        # user.first_name = validated_data['first_name']
        # ...
        # user.set_password(validated_data['password'])

        
        user.save()

        return user



class CousesSerializer(ModelSerializer):
    class Meta:
        model = Couses
        fields = ['id','sub','image','create_date','category']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']



class LessonSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Lesson
        fields = ['id','sub','image','content','create_date','couses',"tags"]



class JoinSerializer(ModelSerializer):
    couses = CousesSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ('name','couses')
        
        
