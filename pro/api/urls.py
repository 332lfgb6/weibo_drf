"""weibo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'weibo', views.WeiboViewSet)
# router.register(r'weibo_images', views.WeiboImageViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'follows', views.FollowViewSet)
router.register(r'user_agree_weibo', views.UserAgreeWeiboViewSet)
router.register(r'add_comment', views.AddCommentViewSet)

urlpatterns = [
  path('temp/', views.Temp.as_view()),
  path('<str:version>/get_code/', views.GetCodeView.as_view()),
  path('<str:version>/get_common/', views.GetCommonApi.as_view()),
  path('<str:version>/login/', views.LoginView.as_view()),
  path('<str:version>/get_user_info_by_token/', views.GetUserInfoByTokenView.as_view()),
  path('<str:version>/get_topic_detail/', views.GetTopicDetailView.as_view()),
  path('<str:version>/get_comment_detail/<int:pk>/', views.GetCommentDetailViewSet.as_view({'get': 'retrieve'})),
  path('<str:version>/get_comment_list/', views.GetCommentListViewSet.as_view({'get': 'list'})),
  path('<str:version>/get_weibo_list/', views.GetWeiboListViewSet.as_view({'get': 'list'})),
  path('<str:version>/get_weibo_detail/<int:pk>/', views.GetWeiboDetailViewSet.as_view({'get': 'retrieve'})),
  path('<str:version>/new_weibo/', views.NewWeiboViewSet.as_view({'post': 'create'})),
  path('<str:version>/new_comment/', views.NewCommentViewSet.as_view({'post': 'create'})),
  path('<str:version>/user_agree_comment/', views.UserAgreeCommentViewSet.as_view({'post': 'create'})),
  path('<str:version>/user_disagree_comment/<int:pk>/', views.UserDisagreeCommentViewSet.as_view({'delete': 'destroy'})),
  path('<str:version>/register/', views.RegisterView.as_view()),
  path('<str:version>/', include(router.urls))
]
