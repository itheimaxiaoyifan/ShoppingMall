from django.db import models

from MeiduoMall.utils.model import BaseModel


class OauthQQUser(BaseModel):
    user = models.ForeignKey('users.User', verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True) # db_index是创建索引,使查询速度变快
    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name

