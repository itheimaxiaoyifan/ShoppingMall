from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from redis import StrictRedis
from rest_framework.response import Response
from rest_framework.views import APIView

from MeiduoMall.libs.yuntongxun.sms import CCP
from MeiduoMall.utils.exceptions import logger
from celery_tasks.sms.tasks import send_sms


class SMScodeView(APIView):
    # /sms_codes/(?P<mobile>1[3-9]\d{9})/
    def get(self, request, mobile):
        """
        :param request: 输入手机号码，点击获取验证码发送验证码API
        :param mobile:
        :return: {'message': 'OK'}
        """
        strict_redis = get_redis_connection('sms_codes')  # type: StrictRedis
        send_flag = strict_redis.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({'message': '发送短信过于频繁'}, status=400)
        # 　1.生成短信验证码
        import random
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info('sms_code: %s' % sms_code)
        #  2.使用云通信发送短信
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # 使用celery来发送短信
        send_sms.delay('13600001111', '213123')
        #  3.保存短信到redis expiry
        # strict_redis.setex('sms_%s_' % mobile, 300, sms_code)  # 5分钟过期
        # strict_redis.setex('send_flag_%s' % mobile, 60, 1)  # 1分钟过期
        #  3.1 使用管道命令优化与redis连接（只需建立一次连接）
        pipeline = strict_redis.pipeline()
        pipeline.setex('sms_%s' % mobile, 300, sms_code)
        pipeline.setex('send_flag_%s' % mobile, 60, 1)
        pipeline.execute()
        return Response({'message': 'OK'})
