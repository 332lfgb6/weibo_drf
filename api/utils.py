from api.models import WeiboImg, Comment, UserAgreeWeibo, Weibo
from api.serializers import WeiboImgSerializer


def add_extra_info(user, weibo):
  weibo_images = WeiboImg.objects.filter(weibo_id=weibo.get('id'))
  weibo_image_serializer = WeiboImgSerializer(weibo_images, many=True)
  weibo.update({'images': weibo_image_serializer.data})
  # self.share_comment_agree(request.user, weibo)

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
  related_weibo = weibo.get('related_weibo')
  if related_weibo:
    related_weibo_id = related_weibo.get('id')
    # 笔记：如果写成weibo，那么需要传递一个weibo对象，所以简单的方式是使用weibo_id。
    weibo_images = WeiboImg.objects.filter(weibo_id=related_weibo_id)
    weibo_image_serializer = WeiboImgSerializer(weibo_images, many=True)
    related_weibo.update({'images': weibo_image_serializer.data})
