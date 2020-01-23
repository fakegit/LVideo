from django.contrib import admin

from LVideo.custom_site import custom_site
from config.models import Links


@admin.register(Links)
@admin.register(Links, site=custom_site)
class LinksAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'created_time']
    fields = ['name', 'link']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面，默认情况下保存按钮在底部
    save_on_top = True
