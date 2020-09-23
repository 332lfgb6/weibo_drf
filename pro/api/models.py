from datetime import datetime

from django.db import models


# 任何网站公共的东西
class Common(models.Model):
  user_agreement = models.TextField()
  privacy_policy = models.TextField()


class Role(models.Model):
  name = models.CharField(max_length=8)


class User(models.Model):
  username = models.CharField(max_length=32, blank=True, null=True)
  password = models.CharField(max_length=15, blank=True, null=True)
  email = models.EmailField(null=True, blank=True, unique=True)
  code = models.CharField(max_length=10, blank=True, null=True)
  token = models.CharField(max_length=64, blank=True, null=True)
  nickname = models.CharField(max_length=15, default='匿名用户')
  gender = models.CharField(max_length=1, default='男')
  birthday = models.DateField(blank=True, null=True)
  blog = models.URLField(blank=True, null=True)
  qq = models.CharField(blank=True, max_length=15, null=True)
  msn = models.CharField(blank=True, max_length=50, null=True)
  brief = models.CharField(max_length=100, default='暂无简介')
  fans = models.PositiveIntegerField(default=0)
  avatar = models.ImageField(upload_to='avatar', default='avatar/default.gif')
  vip_level = models.PositiveSmallIntegerField(default=0)
  closing_time = models.DateTimeField(blank=True, null=True)
  authentication = models.CharField(max_length=5, default='未认证')
  search_by_phone = models.BooleanField(default=True)
  recommend_phone = models.BooleanField(default=True)
  # 所有人，我关注的人，我的粉丝
  who_can_comment = models.CharField(max_length=5, blank=True, null=True)
  # 评论加强
  comment_protect = models.BooleanField(default=False)
  # 收到谁的私信？所有人、我关注的人
  receive_from_user = models.CharField(max_length=5, blank=True, null=True)
  img_comment = models.BooleanField(default=True)
  # 微博可见时间范围？最近半年/全部
  time_range = models.CharField(max_length=4, blank=True, null=True)
  # 同城板块显示我的微博
  same_city_show = models.BooleanField(default=True)
  special_adv = models.BooleanField(default=False)
  province = models.CharField(max_length=5, blank=True, null=True)
  city = models.CharField(max_length=5, blank=True, null=True)
  county = models.CharField(max_length=5, blank=True, null=True)

  def __str__(self):
    return self.nickname


class Follow(models.Model):
  subject = models.ForeignKey('User', models.CASCADE, 'follow_set_subject')
  object = models.ForeignKey('User', models.CASCADE, 'follow_set_object')


class UserBanWeibo(models.Model):
  user = models.ForeignKey('User', models.CASCADE)
  weibo = models.ForeignKey('Weibo', models.CASCADE)
  closing_time = models.DateTimeField()


class Group(models.Model):
  name = models.CharField(max_length=10)
  user = models.ManyToManyField('User', 'group_user_set', blank=True, null=True)


class KeyWordBlackList(models.Model):
  keyword = models.CharField(max_length=15)
  user = models.ManyToManyField('User')


class Category(models.Model):
  name = models.CharField(max_length=5)

  def __str__(self):
    return self.name


class Weibo(models.Model):
  content = models.TextField(default='出bug了')
  pub_time = models.DateTimeField(default=datetime.now)
  update_time = models.DateTimeField(default=datetime.now)
  # 来自...
  f = models.CharField(max_length=32, default='微博 HTML5 版', blank=True, null=True)
  video = models.FileField(upload_to='videos', blank=True, null=True)
  # 视频观看次数
  video_view = models.ManyToManyField('User', 'video_view_set', blank=True, null=True)
  video_time = models.CharField(max_length=8, blank=True, null=True)
  first_image = models.ImageField(upload_to='first_images', blank=True, null=True)
  share = models.PositiveIntegerField(default=0)
  comment_number = models.PositiveIntegerField(default=0)
  category = models.ForeignKey('Category', models.CASCADE, blank=True, null=True)
  topic = models.ManyToManyField('Topic', blank=True, null=True)
  # 用户发微博
  user = models.ForeignKey('User', models.CASCADE, 'user_write_weibo', null=True)
  # 用户收藏微博
  collection = models.ManyToManyField('User', 'user_collect_weibo', blank=True, null=True)
  # 用户赞微博
  user_agree_weibo = models.ManyToManyField('User', 'user_agree_weibo_set', through='UserAgreeWeibo', blank=True,
                                            null=True)
  # 用户屏蔽微博
  user_ban_weibo = models.ManyToManyField('User', 'user_ban_weibo_set', blank=True, null=True)
  # 公开程度：公开 / 好友圈 / 私密
  public_state = models.CharField(max_length=3, default='公开')
  related_weibo = models.ForeignKey('self', models.CASCADE, blank=True, null=True)

  class Meta:
    ordering = ['-id']

  def __str__(self):
    return self.content


# 用户点赞微博
class UserAgreeWeibo(models.Model):
  user = models.ForeignKey('User', models.CASCADE)
  weibo = models.ForeignKey('Weibo', models.CASCADE)


class UserAgreeComment(models.Model):
  user = models.ForeignKey('User', models.CASCADE)
  comment = models.ForeignKey('comment', models.CASCADE)


class Topic(models.Model):
  name = models.CharField(max_length=15, unique=True)
  image = models.ImageField(upload_to='topic_images', blank=True, null=True)


class WeiboImg(models.Model):
  uri = models.ImageField(upload_to='weibo_images')
  weibo = models.ForeignKey('Weibo', models.CASCADE)


class Comment(models.Model):
  content = models.TextField()
  zan = models.PositiveIntegerField(default=0)
  pub_time = models.DateTimeField(default=datetime.now)
  user = models.ForeignKey('User', models.CASCADE, blank=True, null=True)
  parent = models.ForeignKey('self', models.CASCADE, 'comment_set_parent', blank=True, null=True)
  reply_to = models.ForeignKey('self', models.CASCADE, 'comment_set_reply_to', blank=True, null=True)
  weibo = models.ForeignKey('Weibo', models.CASCADE, blank=True, null=True)
  image = models.ImageField(upload_to='comment_images', blank=True, null=True)
  # 用户点赞评论
  user_agree_comment = models.ManyToManyField('User', 'user_agree_comment_set', through='UserAgreeComment', blank=True,
                                              null=True)

  def __str__(self):
    return self.content

  class Meta:
    ordering = '-zan',


# 话题阅读讨论次数
class ReadChat(models.Model):
  user = models.ForeignKey('User', models.CASCADE)
  weibo = models.ForeignKey('Weibo', models.CASCADE)
  topic = models.ForeignKey('Topic', models.CASCADE)
  type = models.CharField(max_length=2, default='阅读')
