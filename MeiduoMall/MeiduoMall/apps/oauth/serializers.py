from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework import serializers

from oauth.models import OauthQQUser
from oauth.utils import check_openid
from users.models import User


class QQUserSerializer(serializers.Serializer):
    """
    :param:mobile,password,sms_code,openid
    :return token,user_id,username
    """
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$', write_only=True)
    password = serializers.CharField(label='密码', max_length=20, min_length=8, write_only=True)
    sms_code = serializers.CharField(label='验证码', max_length=6, write_only=True)
    openid = serializers.CharField(label='openid', max_length=200, write_only=True)

    def validate(self, attrs):
        print(attrs)
        mobile = attrs['mobile']
        password = attrs['password']
        sms_code = attrs['sms_code']
        # 解密openid
        sign_openid = attrs['openid']
        openid = check_openid(sign_openid)
        if not openid:
            raise serializers.ValidationError({'message': '无效的openid'})
        attrs['openid'] = openid
        # 创建redis数据库链接对象
        redis_connection = get_redis_connection('sms_codes')  # type: StrictRedis
        real_sms_codes = redis_connection.get('sms_%s' % mobile)
        if real_sms_codes is None:
            raise serializers.ValidationError({'message': '验证码无效'})
        if real_sms_codes.decode() != sms_code:
            raise serializers.ValidationError({'message': '验证码错误'})
        try:
            # 通过手机号查询数据库，如果不存在则创建用户，如果存在则登录
            user = User.objects.get(mobile=mobile)
            print('user:', user, type(user))
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=mobile,
                password=password,
                mobile=mobile
            )
        else:  # 用户存在
            if not user.check_password(password):
                raise serializers.ValidationError({'message': '密码错误'})
        attrs['user'] = user
        print('attrs:', attrs)
        print('validate结束')
        return attrs

    def create(self, validated_data):
        print('validated_data', validated_data, type(validated_data))
        openid = validated_data.get('openid')
        user = validated_data.get('user')
        qquser = OauthQQUser.objects.create(openid=openid, user=user)
        print('create结束')
        return user
