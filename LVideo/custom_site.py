#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:joel 18-6-5

from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Lvideo'
    site_title = 'Lvideo后台'
    index_title = '首页'


custom_site = CustomSite(name='custom_admin')
