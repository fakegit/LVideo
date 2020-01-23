from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import Source, VideoInfo, VideoLink
from LVideo.custom_site import custom_site


@admin.register(Source)
@admin.register(Source, site=custom_site)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['domin', 'name', 'type', 'is_effect', 'format_page', 'created_time']
    fields = ['domin', 'name', 'is_effect', 'type', 'format_page']

    search_fields = ['domin', 'name']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面，默认情况下保存按钮在底部
    save_on_top = True


@admin.register(VideoInfo)
@admin.register(VideoInfo, site=custom_site)
class VideoInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'alias', 'remark', 'cover_url', 'director', 'actor', 'first_type',
                    'second_type', 'region', 'update_time', 'nums', 'release_time',
                    'source', 'created_time']
    fields = ['name', 'alias', 'remark', 'cover_url', 'director', 'actor', 'first_type',
              'second_type', 'region', 'update_time', 'nums', 'release_time', 'intro',
              'source', 'created_time']

    search_fields = ['name', 'source', 'director', 'actor']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面，默认情况下保存按钮在底部
    save_on_top = True


@admin.register(VideoLink)
@admin.register(VideoLink, site=custom_site)
class VideoLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'number', 'status', 'is_new', 'source', 'created_time']
    fields = ['name', 'link', 'number', 'status', 'is_new', 'source', 'created_time']

    search_fields = ['name', 'source']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面，默认情况下保存按钮在底部
    save_on_top = True


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('object_repr', 'object_id', 'action_flag', 'user', 'change_message', 'action_time')