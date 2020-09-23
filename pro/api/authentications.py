from rest_framework.authentication import BaseAuthentication

from api.models import User


class MyAuthentication(BaseAuthentication):
  def authenticate(self, request):
    token = request.query_params.get('token')
    if token:
      user = User.objects.filter(token=token).first()
      return user, None
    else:
      return None, None
