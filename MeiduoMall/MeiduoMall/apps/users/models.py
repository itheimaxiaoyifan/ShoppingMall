from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    email_active = models.BooleanField(default=False,verbose_name='邮箱认证状态')

class Meta:
    db_table = 'tb_users'  # 表名
    verbose_name = '用户'  # 后台显示的名称
    verbose_name_plural = verbose_name  # 后台显示名称不分单复数






