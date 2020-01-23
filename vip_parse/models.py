from django.db import models


class ParseInterface(models.Model):
    STATUS_NORMAL = 1
    STATUS_UNNORMAL = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '有效地址'),
        (STATUS_UNNORMAL, '无效地址'),
    )

    name = models.CharField(max_length=128, verbose_name='解析名称')
    domin = models.CharField(max_length=128, verbose_name='解析域名')
    parse_url = models.CharField(max_length=512, verbose_name='解析链接')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='是否有效')
    speed = models.PositiveIntegerField(default=1,  verbose_name='解析速度')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '解析接口'

    def __str__(self):
        return self.name

    @classmethod
    def get_interfaces(cls):
        queryset = cls.objects.all().order_by('speed')
        return queryset
