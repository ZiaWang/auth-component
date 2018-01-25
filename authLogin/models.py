from django.db import models


class UserInfo(models.Model):
    """
        用户信息表
    """

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name='登录名')
    password = models.CharField(max_length=64, verbose_name='密码')
    nick_name = models.CharField(max_length=32, verbose_name='昵称')
    join_time = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')
    telephone = models.CharField(max_length=11, verbose_name='手机号', unique=True, null=True)
    email = models.EmailField(verbose_name='联系邮箱')
    avatar = models.FileField(verbose_name='头像', upload_to='avatar', null=True)

    def __str__(self):
        return self.nick_name

    class Meta:
        verbose_name_plural = '用户表'