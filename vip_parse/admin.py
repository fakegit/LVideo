from django.contrib import admin

from LVideo.custom_site import custom_site
from vip_parse.models import ParseInterface


@admin.register(ParseInterface)
@admin.register(ParseInterface, site=custom_site)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['domin', 'name', 'parse_url', 'status', 'speed', 'created_time']
    fields = ['domin', 'name', 'parse_url', 'status', 'speed']

    search_fields = ['domin', 'name']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面，默认情况下保存按钮在底部
    save_on_top = True
