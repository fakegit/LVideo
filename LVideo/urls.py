"""LVideo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from LVideo.custom_site import custom_site
from video.views import IndexView, Latest5View, VideoDetailView, VideoPlayView, MoreListView, VideoPlayIndexView, \
    SearchView, ClickView, register, login, logout
from vip_parse.views import VipParseView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('viparse', VipParseView.as_view(), name='vip-parse'),
    path('latest5', Latest5View.as_view(), name='latest5'),
    path('clicknums', ClickView.as_view(), name='clicknums'),
    path('login', login),
    path('register', register),
    path('logout', logout, name='logout'),
    # path('profile', profile, name='profile'),
    path('search', SearchView.as_view(), name='search'),
    path('dm', MoreListView.as_view(), name='dm-list'),
    path('tv', MoreListView.as_view(), name='tv-list'),
    path('zy', MoreListView.as_view(), name='zy-list'),
    path('mv', MoreListView.as_view(), name='mv-list'),
    path('ot', MoreListView.as_view(), name='ot-list'),
    path('detail/<int:video_id>.html', VideoDetailView.as_view(), name='video-detail'),
    path('playindex/<int:video_id>.html', VideoPlayIndexView.as_view(), name='video-play-index'),
    path('play/<int:video_id>/<int:play_id>.html', VideoPlayView.as_view(), name='video-play'),
    path('super_admin/', admin.site.urls),
    path('custom_admin/', custom_site.urls)
]
