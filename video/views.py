from datetime import date

from django.contrib import messages
from django.core.cache import cache
from django.db.models import Q, F
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from django.shortcuts import HttpResponseRedirect, redirect, render, render_to_response
from django.views.generic.base import View

from custom.models import Custom
from video.models import VideoInfo, VideoLink
from config.models import Links


class CommonUserMixin:
    # @staticmethod
    # def get_username(request):
    #     if 'username' in request.COOKIES:
    #         # 获取cookie中的用户名、密码
    #         username = request.COOKIES['username']
    #         return username
    #     else:
    #         return ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            # 'username': self.get_username(self.request),
            'max_left_item_count': 2
        })
        return context


class CommonListView(CommonUserMixin, ListView):
    queryset = VideoInfo.latest_video()
    context_object_name = 'video_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'max_left_item_count': 2
        })
        return context


class IndexView(CommonListView):
    queryset = VideoInfo.get_type_video_list(VideoInfo.TYPE_DM)[:10]
    context_object_name = 'video_list'
    template_name = 'video/index_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'dm_list': super().get_queryset(),
            'mv_list': VideoInfo.get_type_video_list(VideoInfo.TYPE_MV)[:10],
            'tv_list': VideoInfo.get_type_video_list(VideoInfo.TYPE_TV)[:10],
            'zy_list': VideoInfo.get_type_video_list(VideoInfo.TYPE_ZY)[:10],
            'ot_list': VideoInfo.get_type_video_list(VideoInfo.TYPE_OT)[:10],
            'dm_pv_list': VideoInfo.get_hot_video_list(VideoInfo.TYPE_DM)[:10],
            'mv_pv_list': VideoInfo.get_hot_video_list(VideoInfo.TYPE_MV)[:10],
            'tv_pv_list': VideoInfo.get_hot_video_list(VideoInfo.TYPE_TV)[:10],
            'zy_pv_list': VideoInfo.get_hot_video_list(VideoInfo.TYPE_ZY)[:10],
            'ot_pv_list': VideoInfo.get_hot_video_list(VideoInfo.TYPE_OT)[:10],
            'links': Links.get_links()
        })
        return context


class Latest5View(CommonListView):
    paginate_by = 30
    template_name = 'video/latest5_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'links': Links.get_links(),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()[:300]
        return queryset


class CommonPUView(CommonUserMixin, DetailView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        video_id = self.kwargs.get('video_id')
        self.handle_visited(video_id)
        return response

    def handle_visited(self, v_id):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60)  # 24小时有效

        if increase_pv and increase_uv:
            VideoInfo.objects.filter(pk=v_id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            VideoInfo.objects.filter(pk=v_id).update(pv=F('pv') + 1)
        elif increase_uv:
            VideoInfo.objects.filter(pk=v_id).update(uv=F('uv') + 1)


class VideoDetailView(CommonPUView):
    queryset = VideoInfo.latest_video()
    context_object_name = 'video_detail'
    template_name = 'video/detail.html'
    pk_url_kwarg = 'video_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_id = self.kwargs.get('video_id')
        name = VideoInfo.get_video_name(video_id)
        context.update({
            'video_links': VideoLink.get_video_links(name),
            'links': Links.get_links(),
        })
        return context


class VideoPlayIndexView(CommonPUView):
    queryset = VideoInfo.latest_video()
    context_object_name = 'video_play_index'
    template_name = 'video/playindex.html'
    pk_url_kwarg = 'video_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = VideoInfo.get_video_name(self.kwargs.get('video_id'))
        context.update({
            'video_links': VideoLink.get_video_links(name),
            'links': Links.get_links(),
        })
        return context


class VideoPlayView(CommonPUView):
    queryset = VideoInfo.latest_video()
    context_object_name = 'video_play'
    template_name = 'video/play.html'
    pk_url_kwarg = 'video_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        play_id = self.kwargs.get('play_id')
        name = VideoInfo.get_video_name(self.kwargs.get('video_id'))
        context.update({
            'play_link': VideoLink.get_play_link(play_id),
            'video_links': VideoLink.get_video_links(name),
            'links': Links.get_links(),
        })
        return context


class MoreListView(CommonListView):
    paginate_by = 10
    template_name = 'video/more_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            # 传入导航菜单对应视频类型的菜单名称
            'button': VideoInfo.V_TYPE_LIST[str(self.request.path).replace('/', '')],
            'links': Links.get_links(),
        })
        return context

    def get_queryset(self):
        request_path = str(self.request.path).replace('/', '')
        v_type = VideoInfo.V_TYPE_LIST[request_path]
        queryset = VideoInfo.get_type_video_list(v_type)
        return queryset


class SearchView(CommonListView):
    paginate_by = 10
    template_name = 'video/more_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', ''),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(name__icontains=keyword) | Q(alias__icontains=keyword))


class ClickView(CommonListView):
    template_name = 'video/clicknums.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'links': Links.get_links(),
        })
        return context

    def get_queryset(self):
        """
        根据pv排序，获取前100条播放量大于等于1的的视频
        """
        queryset = super().get_queryset()
        return queryset.filter(pv__gte=1).order_by('-pv')[:100]


def register(request):
    if request.method == "POST" and request.POST:
        data = request.POST
        username = data.get("username")
        email = data.get("email")
        password1 = data.get("password1")
        password2 = data.get("password2")
        custom = Custom.objects.filter(username=username)
        custom_email = Custom.objects.filter(email=email)
        if custom:
            return HttpResponse('{"status": "fail", "msg": "用户名已存在，请重新输入"}')
        if password1 != password2:
            return HttpResponse('{"status": "fail", "msg": "亲~两次密码输入不一致，请重新输入"}')
        if custom_email:  # 邮箱地址唯一
            return HttpResponse('{"status": "fail", "msg": "该邮箱已注册，请换一个邮箱"}')
        else:
            # 注册成功，创建用户
            Custom.objects.create(
                username=username,
                email=email,
                password=Custom.md5_pwd(password1),
            )
            # 重定向到登录页面
            return HttpResponse('{"status": "success", "msg": "注册成功"}')
    else:
        return HttpResponse('{"status": "fail", "msg": "请求失败"}')


def login(request):
    if request.method == 'POST' and request.POST:
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        if username and password:
            custom = Custom.objects.filter(username=username).first()
            if custom:
                now_password = Custom.md5_pwd(password)
                db_password = custom.password
                if now_password == db_password:
                    response = JsonResponse({"status": "success", "msg": "登录成功"})
                    # response.set_cookie('username', username, max_age=7 * 24 * 3600)
                    # response.set_cookie('password', password, max_age=7 * 24 * 3600)
                    # 通过session识别用户并保持用户状态
                    request.session['is_login'] = True
                    request.session['username'] = username
                    return response
                else:
                    return HttpResponse('{"status": "fail", "msg": "密码错误"}')
            else:
                return HttpResponse('{"status": "fail", "msg": "用户不存在"}')
        else:
            return HttpResponse('{"status": "fail", "msg": "用户名或密码为空"}')
    else:
        return HttpResponse('{"status": "fail", "msg": "请求失败"}')


def logout(request):
    if request.session.get('is_login'):
        request.session.flush()
        # flush会一次性清空session中所有内容，可以使用下面的方法
        # del request.session['is_login']
        # del request.session['user_id']
        # del request.session['user_name']
        return redirect("index")

