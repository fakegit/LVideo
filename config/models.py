from django.db import models


class Links(models.Model):
    name = models.CharField(max_length=1024, verbose_name='友链名称')
    link = models.CharField(max_length=512, verbose_name='友链链接', db_index=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '友链'

    def __str__(self):
        return self.name

    @classmethod
    def get_links(cls):
        return cls.objects.all()
