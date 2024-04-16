from rest_framework import serializers as s
from django.contrib.auth.models import User
from .models import New, Comment


class CommentSerializer(s.ModelSerializer):
    
    class Meta:
        
        model = Comment
        fields = '__all__'


class NewSerializer(s.ModelSerializer):
    
    def create(self, validated_data):
        return New.objects.create(**validated_data)

    class Meta:
        model = New
        fields = '__all__'


class UserSerializer(s.ModelSerializer):

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = '__all__'


class NewDetailSerializer(NewSerializer):

    comments = CommentSerializer(many=True)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["comments"] = sorted(response["comments"], key=lambda x: x["created"])[::-1]

        return response


class UserDetailSerializer(UserSerializer):
    created_news = NewSerializer(many=True)
    comments = CommentSerializer(many=True)
