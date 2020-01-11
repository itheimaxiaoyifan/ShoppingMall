import re

from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import User


class CreateUserSerializer(ModelSerializer):
    password2 = serializers.CharField(label='确认密码', min_length=8, max_length=20, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, write_only=True)
    allow = serializers.BooleanField(label='同意协议', default=False, write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            mobile=validated_data.get('mobile')
        )
        # 注册成功自动登录，需要生成jwt并返回给客户端
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # {'user_id': 12, 'email': '', 'username': '13600000000', 'exp': 1539048426}
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token  # 生成的jwt 序列化返回
        return user

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        if not value:
            raise serializers.ValidationError('请同意用户协议')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码输入不一致')
        # 判断短信验证码
        redis_connection = get_redis_connection('sms_codes')  # type: StrictRedis
        mobile = attrs['mobile']
        real_sms_codes = redis_connection.get('sms_%s' % mobile)
        if real_sms_codes is None:
            raise serializers.ValidationError('无效的短信验证码')
        if real_sms_codes.decode() != attrs['sms_code']:
            raise serializers.ValidationError('两次密码不一致')
        return attrs

    class Meta:
        model = User
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的用户名',
                    'max_length': '仅允许8-20个字符的用户名',
                }
            }
        }
        fields = ('id', 'username', 'password', 'mobile',
                  'password2', 'sms_code', 'allow', 'token')
