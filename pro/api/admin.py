from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(User)
admin.site.register(Weibo)
admin.site.register(WeiboImg)
admin.site.register(Topic)
admin.site.register(Comment)
