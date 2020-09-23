from django.db.models import QuerySet
from django_filters import rest_framework as r_filters

from api.models import *
from api.serializers import WeiboSerializer


class WeiboFilter(r_filters.FilterSet):
    """
    过滤器
    """
    # min_price = r_filters.NumberFilter(field_name="shop_price", lookup_expr='gte', label='最小商品价格')
    # max_price = r_filters.NumberFilter(field_name="shop_price", lookup_expr='lte', label='最大商品价格')
    # top_category = r_filters.NumberFilter(method='top_category_filter')
    user = r_filters.NumberFilter(field_name='user', lookup_expr='exact', label='用户ID')
    nickname = r_filters.CharFilter(method='nickname_filter')
    category_id = r_filters.NumberFilter(field_name='category', lookup_expr='exact')
    topic_name = r_filters.CharFilter(method='topic_name_filter')
    keyword = r_filters.CharFilter(field_name='content', lookup_expr='icontains')

    def nickname_filter(self, queryset, name, value):
        user = User.objects.filter(nickname=value).first()
        if not user:
            return []
        weibo_list = queryset.filter(user=user)
        return weibo_list

    def topic_name_filter(self, queryset, name, value):
        topic = Topic.objects.filter(name=value).first()
        if topic:
            return topic.weibo_set.all()
        else:
            return Topic.objects.filter(pk=0)

    # def top_category_filter(self, queryset, name, value):
    #     return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
    #                            Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Weibo
        fields = ('user',)


class CommentFilter(r_filters.FilterSet):
    parent = r_filters.NumberFilter(method='parent_filter')
    weibo = r_filters.NumberFilter(field_name='weibo', lookup_expr='exact', label='微博ID')

    def parent_filter(self, queryset, name, value):
        self
        if value == 0:
            return queryset.filter(parent=None)
        else:
            return queryset.filter(parent=value)

    class Meta:
        model = Comment
        fields = 'parent',
