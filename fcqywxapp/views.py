from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy.utils import check_signature

# 假设你已经从企业微信管理后台获取了Token、EncodingAESKey（对于加密消息是必需的，但验证URL时通常不需要）
TOKEN = 'zGkBNjE-uFVyTPffi-Tsmr88ZgAZvzwDj2w587I84_FH9Sl67rEKpdxsTmgJjDIJzl5vy7TFhn5qQ879_T6LseuoZ6z1mJFbx9zco-gRMYS-UbF4_8OVP1e9WJemiRdxz0yZnDtrz9oV7p2lGZPJDbhLgHm3CdduuD_tSV1nZaVy8AXD6SXMveFyVHrvxNGSps4zVMCyAhjuahwT3c-4IQ'
ENCODING_AES_KEY = '你的EncodingAESKey'  # 如果不需要加密消息，这个可以不设置

# Create your views here.
class qywxrenzheng(APIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        signature = request.GET.get('msg_signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')

        # 验证请求是否来自企业微信
        # 注意：这里只使用了Token进行验证，没有使用EncodingAESKey，因为验证URL时通常不需要加密
        if check_signature(TOKEN, signature, timestamp, nonce):
            return HttpResponse(echostr)  # 验证成功，返回echostr
        else:
            return HttpResponse('Failed to verify request', status=401)  # 验证失败，返回401状态码

