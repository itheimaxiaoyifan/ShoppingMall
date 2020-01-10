# 名字不可更改
from time import sleep
from celery import Celery
from MeiduoMall.libs.yuntongxun.sms import CCP

# 　添加装饰器把函数变成任务
from celery_tasks.main import celery


@celery.task(name='send_sms')
def send_sms(mobile, sms_code):
    print('获取短信验证码')
    sleep(5)
