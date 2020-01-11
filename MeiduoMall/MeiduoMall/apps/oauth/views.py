from QQLoginTool.QQtool import OAuthQQ
from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from oauth.models import OauthQQUser


class QQURLView(APIView):
    """
    提供QQ登录页面地址
    """

    def get(self, request):
        next = request.query_params.get('next')
        # print("next:", next)
        if not next:
            next = '/'
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)
        login_url = oauth.get_qq_url()
        return Response({'login_url': login_url})


class QQUserView(APIView):
    """用户扫码登录的回调处理"""

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code参数'}, status=status.HTTP_400_BAD_REQUEST)
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except:
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        """
        使用openid查询该QQ用户是否在美多商城中绑定过用户
        1.如果没有绑定，返回openid给前端，绑定后再传递给服务器
        2.如果绑定了，查询数据库，返回token,user_id,username给前端
        """
        try:
            qquser = OauthQQUser.objects.get(openid=openid)
        except OauthQQUser.DoesNotExist:
            return Response({'openid': openid})
        else:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            # 获取oauth_user关联的user
            user = qquser.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })
            return response