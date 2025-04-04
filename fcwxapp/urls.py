# myapp/urls.py
from django.urls import path
from .views import (wxrenzheng, send_biaoxian, get_c_s, send_koujian, send_template_message, send_qiandao,
                    get_qiandao_list, qiandao_list, chongzhi, Index)


urlpatterns = [
    path('api/wxrenzheng/', wxrenzheng.as_view(), name='wxrenzheng'),
    path('api/send_template_message/', send_template_message.as_view(), name='send_template_message'),
    path('send_biaoxian/', send_biaoxian.as_view(), name='send_biaoxian'),
    path('send_koujian/', send_koujian.as_view(), name='send_koujian'),
    path('send_qiandao/', send_qiandao.as_view(), name='send_qiandao'),
    path('api/get_c_s/', get_c_s.as_view(), name='get_c_s'),
    path('qiandao_list/', qiandao_list.as_view(), name='qiandao_list'),
    path('api/get_qiandao_list/', get_qiandao_list.as_view(), name='get_qiandao_list'),
    path('chongzhi/', chongzhi.as_view(), name='chongzhi'),
    path('', Index.as_view(), name='index'),
]