#　定义一个ｃｅｌｅｒｙ应用，一个项目只需要一个ｃｅｌｅｒｙ应用
import os

from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MeiduoMall.settings.dev")
# 自定义应用名，任务保存地点
celery = Celery('meiduo', broker='redis://127.0.0.1:6379/15')
celery.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])