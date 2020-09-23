import random
import uuid

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import *
from api.models import *
from api.paginations import *
from api.renderers import *
from api.serializers import *


class WeiboViewSet(viewsets.ModelViewSet):
  serializer_class = WeiboSerializer
  queryset = Weibo.objects.all()
  renderer_classes = [WeiboRenderer]
  pagination_class = TenPageNumberPagination
  filter_backends = DjangoFilterBackend,
  filterset_class = WeiboFilter


class UserAgreeWeiboViewSet(viewsets.ModelViewSet):
  serializer_class = UserAgreeWeiboSerializer
  queryset = UserAgreeWeibo.objects.all()


class Temp(View):
  def post(self, request):
    images = request.FILES.get('images')
    print(type(images), images)
    return HttpResponse('bingo')


# class WeiboImageViewSet(viewsets.ModelViewSet):
#     serializer_class = WeiboImgSerializer
#     queryset = WeiboImg.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         files = request.data.get('files')
#         print(type(files), files)
#         return Response('上传成功')


class CategoryViewSet(viewsets.ModelViewSet):
  serializer_class = CategorySerializer
  queryset = Category.objects.all()


class TopicViewSet(viewsets.ModelViewSet):
  serializer_class = TopicSerializer
  queryset = Topic.objects.all()


class GetCodeView(APIView):
  def post(self, request, *args, **kwargs):
    email = request.data.get('email')
    code = random.randint(100000, 999999)
    try:
      User.objects.create(email=email, code=code)
    except Exception:
      user = User.objects.get(email=email)
      user.code = code
      user.save()
    send_mail('邮箱验证码',
              '本次验证码是：' + str(code),
              '3437281891@qq.com', [email],
              fail_silently=False)
    return Response('验证码发送成功！')


class GetCommonApi(APIView):
  def get(self, request, *args, **kwargs):
    common = Common.objects.first()
    ser = CommonSerializer(common)
    return Response(ser.data)


class LoginView(APIView):
  def post(self, request, *args, **kwargs):
    login_way = request.data.get('loginWay')
    # 判断登录方式是邮箱登录还是账号密码登录
    if login_way == 'email':
      email = request.data.get('email')
      code = request.data.get('code')
      user = User.objects.filter(email=email, code=code).first()
    else:
      username = request.data.get('username')
      password = request.data.get('password')
      user = User.objects.filter(username=username, password=password) \
        .first()
    # 判断验证码是否正确
    if user:
      token = uuid.uuid4()
      user.token = token
      user.save()
      return Response({
        'code': 20,
        'message': '登录成功！',
        'data': {
          'token': token
        }
      })
    else:
      return Response({
        'code': 30,
        'message': '验证码错误'
      })


class GetUserInfoByTokenView(APIView):
  def get(self, request, *args, **kwargs):
    user = User.objects.filter(token=request.query_params.get('token')).first()
    if user:
      ser = UserSerializer(user)
      data = ser.data
      fans_number = Follow.objects.filter(object_id=data['id']).count()
      follower_number = Follow.objects.filter(subject_id=data['id']).count()
      follow_id = Follow.objects.filter(subject=request.user, object_id=data['id']).first()
      data.update({'fans_number': fans_number})
      data.update({'follower_number': follower_number})
      data.update({'follow_id': follow_id})
      return Response(data)


class GetTopicIDView(APIView):
  def get(self, request, *args, **kwargs):
    topic_name = request.query_params.get('topicName')
    topic = Topic.objects.filter(name=topic_name).first()
    if topic:
      return Response(topic.id)


class FollowViewSet(viewsets.ModelViewSet):
  serializer_class = FollowSerializer
  queryset = Follow.objects.all()


# create
class AddCommentViewSet(viewsets.ModelViewSet):
  serializer_class = CommentSerializer
  queryset = Comment.objects.all()
  filter_backends = DjangoFilterBackend,
  filterset_class = CommentFilter
  renderer_classes = CommentRenderer,


class GetCommentDetailViewSet(viewsets.ModelViewSet):
  serializer_class = DepthCommentSerializer
  queryset = Comment.objects.all()
  renderer_classes = GetCommentDetailRenderer,


class GetCommentListViewSet(viewsets.ModelViewSet):
  serializer_class = DepthCommentSerializer
  queryset = Comment.objects.all()
  filter_backends = DjangoFilterBackend,
  filterset_class = CommentFilter
  renderer_classes = DepthCommentRenderer,


class GetWeiboListViewSet(viewsets.ModelViewSet):
  serializer_class = Depth2WeiboSerializer
  queryset = Weibo.objects.all()
  renderer_classes = GetWeiboListRenderer,
  filter_backends = DjangoFilterBackend,
  filter_class = WeiboFilter


class GetWeiboDetailViewSet(viewsets.ModelViewSet):
  serializer_class = Depth2WeiboSerializer
  queryset = Weibo.objects.all()
  renderer_classes = GetWeiboDetailRenderer,


class NewWeiboViewSet(viewsets.ModelViewSet):
  serializer_class = WeiboSerializer
  queryset = Weibo.objects.all()
  renderer_classes = NewWeiboRenderer,


class NewCommentViewSet(viewsets.ModelViewSet):
  serializer_class = CommentSerializer
  queryset = Comment.objects.all()
  renderer_classes = NewCommentRenderer,


class GetTopicDetailView(APIView):
  def get(self, request, *args, **kwargs):
    topic_name = request.query_params.get('topicName')
    topic = Topic.objects.filter(name=topic_name).first()
    if topic:
      read_number = ReadChat.objects.filter(topic=topic, type='阅读').count()
      chat_number = ReadChat.objects.filter(topic=topic, type='讨论').count()
      return Response({
      'code': 20,
      'message': '获取话题细节成功！',
      'data': {
        'topic_name': topic_name,
        'read_number': read_number,
        'chat_number': chat_number
      }
    })
    else:
      return Response({
      'code': 21,
      'message': '该话题不存在',
      'data': {
        'topic_name': topic_name,
        'read_number': 0,
        'chat_number': 0
      }
    })


class UserAgreeCommentViewSet(viewsets.ModelViewSet):
  serializer_class = UserAgreeCommentSerializer
  queryset = UserAgreeComment.objects.all()


class UserDisagreeCommentViewSet(viewsets.ModelViewSet):
  serializer_class = UserAgreeCommentSerializer
  queryset = UserAgreeComment.objects.all()


# 注册用户
class RegisterView(APIView):
  def post(self, request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')
    nickname = request.data.get('nickname')
    avatar = request.data.get('avatar')
    reg_exp = r'^\w{4,8}$'

    if username == '' or password == '':
      return Response('用户名或密码不能为空')

    if not re.match(reg_exp, username):
      return Response('用户名格式错误')

    if not re.match(reg_exp, password):
      return Response('密码格式错误')

    user = User.objects.filter(username=username).first()
    if user:
      return Response('该用户名已被注册')

    user = User.objects.filter(nickname=nickname).first()
    if user:
      return Response('该昵称已被占用')

    token = uuid.uuid4()
    User.objects.create(username=username, nickname=nickname, password=password, token=token, avatar=avatar)

    return Response({
      'code': 700,
      'message': '注册成功',
      'token': token
    })
