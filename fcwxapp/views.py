import time
from datetime import datetime
import hashlib
import json

from xml.etree import ElementTree as ET
import requests

from fcwxapp import wxapi

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

from fcwxapp.models import WeChatToken, StudentProfile, HostClass

WECHAT_TOKEN = 'naye1204'
# appid = 'wx34415bfb0ed72501'
# secret = '1318885b637b49c81faeab40350c1ddb'
# WECHAT_TEMPLATE_ID = '4gKKe-4hEM49-nFSoW5IsStMN0byzKhq8AW0MzoAhvg'
appid = 'wx92ff9310623895e6'
secret = 'fe131033e9bb9ee8a3aaaf4e7f7a67d9'
WECHAT_TEMPLATE_ID = "O-qPMkCKxpjElH8AiT8qQinDpOi-2nBy_ZldXq1YmXE"
OPEN_ID = "ocswY6dZJ-0UJNBi0F_XNkQZweyM"

class wxrenzheng(APIView):
    def get(self, request, *args, **kwargs):

        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        # 将token、timestamp、nonce三个参数进行字典序排序
        tmp_list = [WECHAT_TOKEN, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)

        # 计算并比对signature
        tmp_str_md5 = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
        print(tmp_str_md5)
        if tmp_str_md5 == signature:
            # 验证成功，返回echostr
            return HttpResponse(echostr)
        else:
            # 验证失败，返回错误信息（可选）
            return JsonResponse({'errcode': 40001, 'errmsg': 'Invalid signature'}, status=403)

    def post(self, request, *args, **kwargs):
        """
        这是一个简单的POST请求的APIView示例（尽管在这个例子中我们没有实际处理POST数据）。
        """
        # 处理来自微信服务器的 POST 请求（包括菜单点击事件）
        try:
            # 获取POST请求的原始数据
            xml_data = request.body.decode('utf-8')
            # 解析XML数据
            root = ET.fromstring(xml_data)

            # 提取事件类型和事件键
            event = root.find('Event').text
            event1 = root.find('FromUserName').text
            print(event1)
            event_key = root.find('EventKey').text if root.find('EventKey') is not None else None

            # 判断是否是菜单点击事件
            if event == 'CLICK' and event_key:
                # 根据event_key的值回复不同的文本消息
                if event_key == 'getinfo':
                    response_msg = '<h1>方辰托管</h1><br><a href="www.baidu.com">百度</a>'
                elif event_key == 'MENU_KEY_2':
                    response_msg = '你点击了菜单项2'
                else:
                    response_msg = '未知的菜单项'

                    # 构造回复的XML数据
                xml_response = '''  
                        <xml>  
                        <ToUserName><![CDATA[{to_user}]]></ToUserName>  
                        <FromUserName><![CDATA[{from_user}]]></FromUserName>  
                        <CreateTime>{create_time}</CreateTime>  
                        <MsgType><![CDATA[text]]></MsgType>  
                        <Content><![CDATA[{content}]]></Content>  
                        </xml>  
                        '''.format(
                    to_user=root.find('FromUserName').text,
                    from_user=root.find('ToUserName').text,
                    create_time=int(time.time()),
                    content=response_msg
                )

                return HttpResponse(xml_response, content_type='application/xml')

                # 其他事件处理...

        except Exception as e:
            print(f"Error processing WeChat request: {e}")
            return HttpResponse(status=500)

        return HttpResponse(status=405)  # Method Not Allowed


class send_template_message(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        if data['mark'] == 'qiandao':
            student = StudentProfile.objects.get(archive_number=str(data['thing13']['value']))
            print(student.name)
            student.remaining_classes -= 2
            student.meal_balance -= 10
            student.save()

            WECHAT_TEMPLATE_ID = 'uMxnjUyReUfRl5T3RswRIV6eZsKJU-LOHl2N61lzrRs'
            data['thing11'] = {"value": f"消耗2课时，剩余{student.remaining_classes}课时" }
            data['phrase3'] = {"value": '托管'}
            data['thing21'] = {"value": F"餐费剩余{student.meal_balance}元。"}
            data['time22'] = {"value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            data['thing13'] = {"value":student.name}
            OPEN_ID = student.parent_openid

        # open_id = 'oCvGS6Unqsz2vVBPezahRATfUWHM'
        open_id = OPEN_ID
        template_id = WECHAT_TEMPLATE_ID  # 你的模板ID
        # ... 其他数据，如模板消息的各个字段的值 ...

        # 获取access_token
        access_token = wxapi.get_access_token(appid, secret)
        # 构造发送模板消息的请求体
        post_data = {
            "touser": open_id,
            "template_id": template_id,
            "url": "http://weixin.qq.com/download",
            "miniprogram": {

            },
            "client_msg_id": "",
            "data": data
        }
        print(post_data)
        # 发送POST请求到公众号服务器的模板消息接口
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
        response = requests.post(url, json=post_data)
        print(url)

        # 处理响应
        if response.status_code == 200:
            result = response.json()
            if result['errcode'] == 0:
                return JsonResponse({'status': 'success', 'message': '模板消息发送成功'})
            else:
                return JsonResponse({'status': 'error', 'message': result['errmsg']}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': '发送模板消息失败'}, status=500)


class get_c_s(APIView):
    """
    获取班级和学生信息
    """

    def get(self, request, *args, **kwargs):
        students = StudentProfile.objects.all()
        classes = HostClass.objects.all()

        stujs = {
            "classes": []

        }
        for cls in classes:
            class_data = {
                "classId": cls.id,
                "className": cls.name,
                "students": []
            }
            for stu in students:
                i = 0
                student_data = {
                    "index":i+1,
                    "studentId": stu.archive_number,
                    "name": stu.name,
                    "gender": stu.gender,
                    "canfeiyue": stu.meal_balance,
                    "keshiyue": stu.remaining_hours,
                    "checkedTimes":["上午","下午","午餐"]
                }
                if stu.host_class_id == cls.id:
                    class_data["students"].append(student_data)
            stujs["classes"].append(class_data)

        return JsonResponse(stujs)


class send_biaoxian(APIView):
    """
    发送表现通知
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'biaoxian.html')


class send_koujian(APIView):
    """
    发送扣减通知
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'koujian.html')




class send_qiandao(APIView):
    """
    发送扣减通知
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'qiandao.html')
