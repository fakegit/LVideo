from django.views.generic import ListView

from config.models import Links
from video.views import CommonUserMixin
from vip_parse.models import ParseInterface


class VipParseView(CommonUserMixin, ListView):
    queryset = ParseInterface.get_interfaces()
    context_object_name = 'parse_interfaces'
    template_name = 'video/vip_parse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'links': Links.get_links(),
        })
        return context

