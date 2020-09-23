import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import *


class WeiboSerializer(serializers.ModelSerializer):
  class Meta:
    model = Weibo
    fields = '__all__'


class Depth2WeiboSerializer(serializers.ModelSerializer):
  class Meta:
    model = Weibo
    fields = '__all__'
    depth = 2


class TopicSerializer(serializers.ModelSerializer):
  class Meta:
    model = Topic
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'


class DepthCommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'
    depth = 1


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
  class Meta:
    model = Follow
    fields = '__all__'


class UserAgreeWeiboSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserAgreeWeibo
    fields = '__all__'


class UserAgreeCommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserAgreeComment
    fields = '__all__'


class CommonSerializer(serializers.ModelSerializer):
  class Meta:
    model = Common
    fields = '__all__'


class WeiboImgSerializer(serializers.ModelSerializer):
  class Meta:
    model = WeiboImg
    fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'


class RegisterSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate_username(self, value):
    if not re.match(r'^\w{4,8}$', value):
      return ValidationError('用户名格式不正确')
    return value

  def validate_password(self, value):
    if not re.match(r'^\w{4,8}$', value):
      return ValidationError('密码格式不正确')
    return value
