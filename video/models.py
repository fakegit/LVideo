from django.db import models


class Source(models.Model):
    STATUS_NORMAL = 1
    STATUS_UNNORMAL = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '有效地址'),
        (STATUS_UNNORMAL, '无效地址'),
    )
    TYPE_ZIYUAN = 1
    TYPE_JIEXI = 0
    TYPE_ITEMS = (
        (TYPE_ZIYUAN, '资源类'),
        (TYPE_JIEXI, '解析类'),
    )

    domin = models.CharField(max_length=128, verbose_name='来源域名')
    name = models.CharField(max_length=128, verbose_name='来源名称')
    type = models.PositiveIntegerField(default=TYPE_ZIYUAN, choices=TYPE_ITEMS, verbose_name='来源类型')
    is_effect = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='是否有效')
    format_page = models.CharField(max_length=512, verbose_name='构造初始爬取页链接')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '来源'

    def __str__(self):
        return self.name


class VideoInfo(models.Model):
    TYPE_DM, TYPE_MV, TYPE_TV, TYPE_ZY, TYPE_OT = '动漫', '电影', '电视剧', '综艺', '其他'
    V_TYPE_LIST = {
        'dm': TYPE_DM,
        'mv': TYPE_MV,
        'tv': TYPE_TV,
        'zy': TYPE_ZY,
        'ot': TYPE_OT
    }
    name = models.CharField(max_length=512, verbose_name='视频名称', db_index=True)
    alias = models.CharField(max_length=512, verbose_name='别名', db_index=True)
    remark = models.CharField(max_length=512, verbose_name='视频备注')
    cover_url = models.CharField(max_length=512, verbose_name='封面链接')
    director = models.CharField(max_length=512, verbose_name='导演')
    actor = models.CharField(max_length=1024, verbose_name='演员')
    first_type = models.CharField(max_length=256, verbose_name='视频类别1')
    second_type = models.CharField(max_length=256, verbose_name='视频类别2')
    region = models.CharField(max_length=256, verbose_name='地区')
    update_time = models.CharField(max_length=128, verbose_name='资源更新时间')
    nums = models.PositiveIntegerField(default=1, verbose_name='总集数')
    release_time = models.CharField(max_length=64, verbose_name='上映年份', db_index=True)
    intro = models.TextField(verbose_name='简介')
    source = models.CharField(max_length=128, verbose_name='来源网站名称')
    created_time = models.CharField(max_length=128, verbose_name='创建时间')

    pv = models.PositiveIntegerField(default=1, verbose_name='页面访问量')
    uv = models.PositiveIntegerField(default=1, verbose_name='独立访客数')

    class Meta:
        verbose_name = verbose_name_plural = '视频信息'

    def __str__(self):
        return self.name

    @classmethod
    def get_type_video_list(cls, v_type):
        """
        返回相关first_type的所有video，并根据update_time倒序
        """
        queryset = cls.objects.filter(first_type=v_type).order_by('-update_time')
        return queryset

    @classmethod
    def get_hot_video_list(cls, v_type):
        """
        返回相关first_type的所有video，并根据pv倒序
        """
        queryset = cls.objects.filter(first_type=v_type).order_by('-pv')
        return queryset

    @classmethod
    def get_video_name(cls, video_id):
        name_list = cls.objects.filter(id=video_id).values('name')
        # 返回的name_list是 <QuerySet [{'name':xxx},]>
        name = name_list[0].get('name')
        return name

    @classmethod
    def latest_video(cls):
        queryset = cls.objects.all().order_by('-update_time')
        return queryset

    @classmethod
    def get_video_pu(cls, v_name):
        v_pu = cls.objects.filter(name=v_name)[0]
        return v_pu


class VideoLink(models.Model):
    STATUS_NORMAL = 1
    STATUS_UNNORMAL = 0
    NEW = 1
    UNNEW = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '有效链接'),
        (STATUS_UNNORMAL, '无效链接'),
    )
    IS_NEW_ITEMS = (
        (NEW, '最新一集'),
        (UNNEW, '非最新一集'),
    )
    name = models.CharField(max_length=1024, verbose_name='视频名称')
    link = models.CharField(max_length=512, verbose_name='视频链接', db_index=True)
    number = models.CharField(max_length=128, verbose_name='当前视频集数')
    is_new = models.PositiveIntegerField(default=UNNEW, choices=IS_NEW_ITEMS, verbose_name='是否最新一集')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='是否有效链接')
    source = models.CharField(max_length=128, verbose_name='来源网站名称')
    created_time = models.CharField(max_length=128, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '视频播放链接'

    def __str__(self):
        return self.link

    @classmethod
    def get_video_links(cls, name):
        video_links = cls.objects.filter(name=name).order_by('number')
        return video_links

    @classmethod
    def get_play_link(cls, play_id):
        play_link = cls.objects.filter(id=play_id)[0]
        return play_link



#
# CREATE TABLE `source` (
#   `source_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '来源网站ID',
#   `source_domin` varchar(20) NOT NULL COMMENT '来源网站域名',
#   `source_name` varchar(128) NOT NULL COMMENT '来源网站名称（英）',
#   `source_type` varchar(256) DEFAULT NULL COMMENT '网站类型',
#   `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`source_id`),
#   KEY `source_name` (`source_name`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
#
#
# CREATE TABLE `v_info` (
#   `v_id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '视频ID',
#   `v_name` varchar(512) NOT NULL COMMENT '视频名称',
#   `v_alias` varchar(512) DEFAULT NULL COMMENT '别名',
#   `v_cover_url` varchar(512) DEFAULT NULL COMMENT '封面链接',
#   `v_director` varchar(256) DEFAULT NULL COMMENT '导演',
#   `v_actor` varchar(512) DEFAULT NULL COMMENT '演员',
#   `v_type` varchar(256) DEFAULT NULL COMMENT '视频类型',
#   `v_region` varchar(256) DEFAULT NULL COMMENT '地区',
#   `v_update_time` datetime DEFAULT NULL COMMENT '更新时间',
#   `v_nums` int(10) unsigned DEFAULT NULL COMMENT '集数',
#   `v_release_time` datetime DEFAULT NULL COMMENT '上映时间',
#   `v_intro` text COMMENT '简介',
#   `source_name` varchar(256) DEFAULT NULL COMMENT '来源网站名称',
#   `created_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`v_id`),
#   KEY `v_name` (`v_name`) USING BTREE,
#   KEY `v_release_time` (`v_release_time`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
