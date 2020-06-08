from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from app.models import User


class CustomAuthToken(ObtainAuthToken):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if not user:
            return Response({'data': '用户不存在或者密码错误'}, status.HTTP_403_FORBIDDEN)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 生成载荷信息(payload),根据user的信息生成一个payload
        payload = jwt_payload_handler(user)
        # 根据payload和secret_key，采用HS256，生成token.
        token = jwt_encode_handler(payload)
        data = {
            'token': token,
            'username': user.username,
            'userId': user.id
        }
        return Response({'data': data}, status.HTTP_201_CREATED)


@api_view(['post'])
@permission_classes([AllowAny])
def create(request):  # Register
    data = request.data  # The passed data is serialized to json

    same_name_user = User.objects.filter(username=data["username"])
    if same_name_user:  # Determine whether there is the same user, that is, the registered email
        message = '用户名已被注册！'
        return Response({'data': message}, status.HTTP_403_FORBIDDEN)
    user_model = get_user_model()
    user = user_model.objects.create_user(username=data["username"], password=data["password"])
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    # 生成载荷信息(payload),根据user的信息生成一个payload
    payload = jwt_payload_handler(user)
    # 根据payload和secret_key，采用HS256，生成token.
    token = jwt_encode_handler(payload)
    data = {
        'token': token,
        'username': user.username,
        'userId': user.id
    }
    return Response({'data': data}, status.HTTP_201_CREATED)
