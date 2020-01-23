import hashlib

from django.db import models


class Custom(models.Model):
    username = models.CharField(max_length=512, verbose_name='用户名')
    password = models.CharField(max_length=512, verbose_name='密码')
    email = models.EmailField(max_length=512, verbose_name='邮箱')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    @classmethod
    def md5_pwd(cls, password):
        """
        加密密码，算法单次md5
        """
        md5 = hashlib.md5()
        # 加盐
        password += 'lvideo'
        md5.update(password.encode())
        password = md5.hexdigest()
        return str(password)

