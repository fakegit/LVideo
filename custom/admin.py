from django.contrib import admin

from custom.models import Custom


@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'email', 'created_time']
    fields = ['username', 'password', 'email', 'created_time']

    search_fields = ['username']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面，默认情况下保存按钮在底部
    save_on_top = True
