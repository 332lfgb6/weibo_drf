from django.core.files import File
from django.db.models import Max
from rest_framework import renderers

from api.models import *
from api.serializers import *
from api.utils import *


class WeiboRenderer(renderers.JSONRenderer):
  # 追加转发、评论、点赞数据
  def share_comment_agree(self, user, weibo):
    self
    # 追加评论数量
    # 超级注意这里，可能发现华点
    comment_number = Comment.objects.filter(weibo=weibo.get('id')).count()
    weibo.update({'commentNumber': comment_number})
    # 追加点赞数量
    agree_number = UserAgreeWeibo.objects.filter(weibo=weibo.get('id')).count()
    weibo.update({'agreeNumber': agree_number})
    # 追加转发数量
    share_number = Weibo.objects.filter(related_weibo=weibo.get('id')).count()
    weibo.update({'shareNumber': share_number})
    # 追加用户点赞微博ID
    if user:
      user_agree_weibo = UserAgreeWeibo.objects.filter(user=user, weibo=weibo.get('id')).first()
      if user_agree_weibo:
        weibo.update({'userAgreeWeiboID': user_agree_weibo.id})

  def render(self, data, accepted_media_type=None, renderer_context=None):
    request = renderer_context['request']
    method = request.method
    path = request.path
    # 写微博/转发微博
    if method == 'POST':
      weibo = Weibo.objects.get(id=data.get('id'))
      # 关联用户
      weibo.user = request.user
      weibo.save()
      # 处理上传过来的图片
      images = request.data.getlist('images')
      weibo_images = [WeiboImg(weibo=weibo, uri=image) for image in images]
      WeiboImg.objects.bulk_create(weibo_images)
      # 转发微博需要指定关联的微博
      related_weibo_id = request.data.get('related_weibo')
      weibo.related_weibo = Weibo.objects.get(id=related_weibo_id)
      weibo.save()
    # 获取首页微博列表
    elif method == 'GET' and request.path == '/api/v1/weibo/':
      weibo_list = data.get('results')
      for weibo in weibo_list:
        # 加入九宫格图片
        weibo_images = WeiboImg.objects.filter(weibo_id=weibo.get('id'))
        weibo_image_serializer = WeiboImgSerializer(weibo_images, many=True)
        weibo.update({'images': weibo_image_serializer.data})
        self.share_comment_agree(request.user, weibo)
      data.update({'results': weibo_list})
      keyword = request.query_params.get('keyword')
      if keyword:
        users = User.objects.filter(nickname__icontains=keyword)
        if users:
          max_fans = users.aggregate(Max('fans')).get('fans__max')
          user = users.filter(fans=max_fans).first()
          ser = UserSerializer(user)
          data.update({'user_info': ser.data})
    elif method == 'GET' and request.path != '/api/v1/weibo/':
      weibo = Weibo.objects.get(id=data.get('id'))
      weibo_images = WeiboImg.objects.filter(weibo=weibo)
      weibo_image_serializer = WeiboImgSerializer(weibo_images, many=True)
      data.update({'images': weibo_image_serializer.data})
    return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)


class GetWeiboListRenderer(renderers.JSONRenderer):
  def render(self, data, accepted_media_type=None, renderer_context=None):
    request = renderer_context['request']
    method = request.method
    current_user = request.user
    
    for weibo in data:
      add_extra_info(request.user, weibo)
      if current_user:
        follow = Follow.objects.filter(subject_id=current_user.id, object_id=weibo['user']['id']).first()
        if follow:
          weibo['user'].update({'follow_id': follow.id})
    newData = {}
    newData.update({'weiboList': data})

    # 根据微博正文内容搜索的时候，需要把粉丝最多的用户给显示出来
    keyword = request.query_params.get('keyword')
    if keyword:
      user = User.objects.filter(nickname__icontains=keyword).first()
      user_serializer = UserSerializer(user)
      return_dict = dict(user_serializer.data)

      # 如果已经登录
      if current_user:
        follow = Follow.objects.filter(subject_id=current_user.id, object_id=user.id).first()
        if follow:
          return_dict.update({'follow_id': follow.id})
      newData.update({'user': return_dict})

    # 访问晚霞用户信息页的时候，会有一个nickname传过来，这个时候，返回微博列表的时候，还需要把该nickname对应的用户信息返回到前端，
    nickname = request.query_params.get('nickname')
    if nickname:
      user = User.objects.filter(nickname=nickname).first()
      user_serializer = UserSerializer(user)
      return_dict = dict(user_serializer.data)
      if request.user:
        print('zzzzzzzzzzz', request.user)
        follow = Follow.objects.filter(subject_id=request.user.id, object_id=user.id).first()
        if follow:
          return_dict.update({'follow_id': follow.id})

      # 绑定粉丝数量、关注者数量和follow_id
      nickname = request.query_params.get('nickname')
      user = User.objects.filter(nickname=nickname).first()
      if user:
        fans_number = Follow.objects.filter(object_id=user.id).count()
        follower_number = Follow.objects.filter(subject_id=user.id).count()
        follow = Follow.objects.filter(subject=request.user, object_id=user.id).first()
        return_dict.update({'fans_number': fans_number})
        return_dict.update({'follower_number': follower_number})
        if follow:
          return_dict.update({'follow_id': follow.id})

      newData.update({'user': return_dict})
    return super().render(newData, accepted_media_type=accepted_media_type, renderer_context=renderer_context)


class GetWeiboDetailRenderer(renderers.JSONRenderer):
  def render(self, data, accepted_media_type=None, renderer_context=None):
    request = renderer_context['request']
    add_extra_info(request.user, data)
    weibo_id = data['id']

    # 阅读次数+1
    user = request.user
    if user:
      for topic in data['topic']:
        read_chat = ReadChat.objects.filter(type='阅读', weibo_id=weibo_id, topic_id=topic['id'], user=user).first()
        if not read_chat:
          ReadChat.objects.create(type='阅读', weibo_id=data['id'], topic_id=topic['id'], user=user)

    # 整合转发、评论、点赞数量
    share_number = Weibo.objects.filter(related_weibo=weibo_id).count()
    comment_number = Comment.objects.filter(weibo_id=weibo_id).count()
    agree_number = UserAgreeWeibo.objects.filter(weibo_id=weibo_id).count()
    new_data = dict(data)
    new_data.update({'share_number': share_number})
    new_data.update({'comment_number': comment_number})
    new_data.update({'agree_number': agree_number})

    return super().render(new_data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)


class NewWeiboRenderer(renderers.JSONRenderer):

  def render(self, data, accepted_media_type=None, renderer_context=None):
    request = renderer_context.get('request')
    images = request.data.getlist('images')
    print(type(images), images)
    weibo_id = data.get('id')
    weibo_images = [WeiboImg(uri=image, weibo_id=weibo_id) for image in images]
    WeiboImg.objects.bulk_create(weibo_images)

    # 关联微博和话题，如果没有该话题，则新建。
    topic_names = request.data.getlist('topic_name')
    for topic_name in topic_names:
      try:
        topic = Topic.objects.create(name=topic_name)
      except:
        topic = Topic.objects.get(name=topic_name)
      weibo = Weibo.objects.get(id=weibo_id)
      weibo.topic.add(topic)

      # 讨论次数+1
      user = request.user
      read_chat = ReadChat.objects.filter(user=user, topic=topic, weibo=weibo, type='讨论').first()
      if not read_chat:
        ReadChat.objects.create(user=user, topic=topic, weibo=weibo, type='讨论')
    return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)

class NewCommentRenderer(renderers.JSONRenderer):

  def render(self, data, accepted_media_type=None, renderer_context=None):
    request = renderer_context.get('request')
    image = request.data.get('images')
    comment_id = data.get('id')
    print(type(comment_id), comment_id)
    comment = Comment.objects.get(id=comment_id)
    print(type(comment), comment)
    comment.image = image
    comment.save()
    return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)


class CommentRenderer(renderers.JSONRenderer):
  def render(self, data, accepted_media_type=None, renderer_context=None):
    return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)


class GetCommentDetailRenderer(renderers.JSONRenderer):
  def render(self, data, accepted_media_type=None, renderer_context=None):

    # 获取这条评论赞的数量
    agree_number = UserAgreeComment.objects.filter(comment_id=data['id']).count()
    data.update({'agree_number': agree_number})

    # 判断当前用户是否赞过
    request = renderer_context['request']
    user_agree_comment_id = UserAgreeComment.objects.filter(comment_id=data['id'], user=request.user).first()
    if user_agree_comment_id:
      data.update({'user_agree_comment_id': user_agree_comment_id.id})

    return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)


class DepthCommentRenderer(renderers.JSONRenderer):
  def render(self, data, accepted_media_type=None, renderer_context=None):
    request = renderer_context.get('request')
    for root_comment in data:
      root_comment_id = root_comment.get('id')
      child_comment_number = Comment.objects.filter(parent=root_comment_id).count()
      root_comment.update({'child_comment_number': child_comment_number})

      # 获取这条评论赞的数量
      agree_number = UserAgreeComment.objects.filter(comment_id=root_comment_id).count()
      root_comment.update({'agree_number': agree_number})

      # 判断当前用户是否赞过
      user_agree_comment_id = UserAgreeComment.objects.filter(comment_id=root_comment_id, user=request.user).first()
      if user_agree_comment_id:
        root_comment.update({'user_agree_comment_id': user_agree_comment_id.id})

    parent = request.query_params.get('parent')
    return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)


class GetUserInfoRenderer(renderers.JSONRenderer):
  def render(self, data, accepted_media_type=None, renderer_context=None):
    fans_number = Follow.objects.filter(object_id=data['id']).count()
    follower_number = Follow.objects.filter(subject_id=data['id']).count()
    request = renderer_context['request']
    follow_id = Follow.objects.filter(subject=request.user, object_id=data['id']).first()
    data.update({'fans_number': fans_number})
    data.update({'follower_number': follower_number})
    data.update({'follow_id': follow_id})
    return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
