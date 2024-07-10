import json

from django.utils import timezone
from .models import WeChatToken
import requests


def fetch_and_store_access_token(appid, secret):
    # 构造获取access_token的URL
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    response = requests.get(url)
    data = response.json()
    print(data)
    if 'access_token' in data:
        # 假设微信还返回了expires_in字段，表示token的过期时间（秒）
        expires_in = data.get('expires_in', 7200)  # 默认2小时
        expires_at = timezone.now() + timezone.timedelta(seconds=expires_in)

        # 检查是否已经存在这个appid的token记录
        token_obj, created = WeChatToken.objects.update_or_create(
            appid=appid,
            defaults={
                'access_token': data['access_token'],
                'expires_at': expires_at,
            }
        )

        if not created:
            # 如果不是新创建的，你可能还想更新expires_at或其他字段
            token_obj.expires_at = expires_at
            token_obj.save()

        return token_obj.access_token
    else:
        # 处理错误...
        return None


def get_access_token(appid,secret):
    try:
        token_obj = WeChatToken.objects.get(appid=appid)
        # 检查token是否过期，如果过期则重新获取（这里只是一个简单的示例，你可能需要更复杂的逻辑）
        if token_obj.expires_at and token_obj.expires_at > timezone.now():
            acctocken = token_obj.access_token

        else:
            acctocken = fetch_and_store_access_token(appid, secret)
        return acctocken
    except WeChatToken.DoesNotExist:
        acctocken = fetch_and_store_access_token(appid, secret)
        return acctocken


def send_template_message(access_token, touser, template_id, data):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    headers = {'Content-Type': 'application/json'}
    data = {
        "touser": touser,
        "template_id": template_id,
        "data": data,  # 这里是上面提到的模板数据的字典
        # 可以根据需要添加其他字段，如 "url"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()