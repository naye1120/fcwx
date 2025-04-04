import time
from datetime import datetime
import hashlib
import json
from decimal import Decimal

from xml.etree import ElementTree as ET
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from fcwxapp import wxapi

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

from fcwxapp.models import WeChatToken, StudentProfile, HostClass, StudentRecord, RechargeRecord

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
            print(event)
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
            for stu in request.data['students']:
                student = StudentRecord.objects.filter(file_number=stu['studentId']).last()
                # student.remaining_classes -= 2
                # student.meal_balance -= 10
                # student.save()

                WECHAT_TEMPLATE_ID = 'uMxnjUyReUfRl5T3RswRIV6eZsKJU-LOHl2N61lzrRs'
                data['thing11'] = {"value": f"本次变化{student.changed_hours}课时，剩余{student.remaining_hours}课时"}
                data['phrase3'] = {"value": '托管签到'}
                data['thing21'] = {"value": F"餐费剩余{student.meal_balance}元。"}
                data['time22'] = {"value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                data['thing13'] = {"value": student.student_name}
                OPEN_ID = StudentProfile.objects.get(archive_number=stu['studentId']).parent_openid

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
                mess = wxapi.sene_tem(access_token=access_token, post_data=post_data)
        elif data['mark'] == 'gengxin':
            studentid = data['thing13']['value']
            print(studentid)
            student = StudentRecord.objects.filter(file_number=studentid).last()
            print(student.student_name)
            # student.remaining_classes -= 2
            # student.meal_balance -= 10
            # student.save()
            if student:
                WECHAT_TEMPLATE_ID = 'uMxnjUyReUfRl5T3RswRIV6eZsKJU-LOHl2N61lzrRs'
                data['thing11'] = {"value": f"本次变化{student.changed_hours}课时，剩余{student.remaining_hours}课时"}
                data['phrase3'] = {"value": '更新课时'}
                data['thing21'] = {"value": F"餐费剩余{student.meal_balance}元。"}
                data['time22'] = {"value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                data['thing13'] = {"value": student.student_name}
                OPEN_ID = StudentProfile.objects.get(archive_number=studentid).parent_openid

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
                mess = wxapi.sene_tem(access_token=access_token, post_data=post_data)
        elif data['mark'] == 'chongzhi':
            studentid = data['student_name']['value']
            studentrecord = RechargeRecord.objects.filter(file_number=studentid).last()
            student = StudentProfile.objects.filter(archive_number=studentid).last()
            # student.remaining_classes -= 2
            # student.meal_balance -= 10
            # student.save()
            if studentrecord:
                WECHAT_TEMPLATE_ID = 'MHF71QznwMs6My3teFlQv4Qk8jUMmG3c1wLw6B487zY'
                data['phrase1'] = {"value": studentrecord.student_name}
                data['character_string14'] = {"value":studentrecord.recharge_hours}
                data['character_string12'] = {"value": student.remaining_hours}
                data['time4'] = {"value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                data['thing16'] = {"value": f'餐费：充{studentrecord.recharge_meal_fee}，余：{student.meal_balance}'}
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
                    "url": "",
                    "miniprogram": {

                    },
                    "client_msg_id": "",
                    "data": data
                }
                mess = wxapi.sene_tem(access_token=access_token, post_data=post_data)
        return mess


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
                    "index": i + 1,
                    "studentId": stu.archive_number,
                    "name": stu.name,
                    "gender": stu.gender,
                    "canfeiyue": stu.meal_balance,
                    "keshiyue": stu.remaining_hours,
                    "checkedTimes": ["上午", "下午", "午餐"],
                    "beizhu": ""
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

    def post(self, request, *args, **kwargs):

        oc_time = request.data['time22']['value']
        studentid = request.data['thing13']['value']
        student_name = request.data['thing13']['name']
        note = request.data['beizhu']
        moring = request.data['morning']
        afternoon = request.data['afternoon']
        lunch = request.data['lunch']
        studenrecord = StudentRecord.objects.filter(file_number=studentid, oc_time=oc_time).last()
        student = StudentProfile.objects.filter(archive_number=studentid).last()
        koujian = 0
        wucan = 0
        # keshiyue = student.remaining_hours
        # wucanyue = student.meal_balance
        if studenrecord:
            if moring > studenrecord.morning:
                koujian += 1
            elif moring < studenrecord.morning:
                koujian -= 1
            if afternoon > studenrecord.afternoon:
                koujian += 1
            elif afternoon < studenrecord.afternoon:
                koujian -= 1
            if lunch > studenrecord.lunch:
                wucan += 10
            elif lunch < studenrecord.lunch:
                wucan -= 10
            keshiyue = student.remaining_hours - koujian
            print(keshiyue)
            wucanyue = student.meal_balance -wucan
            print(wucanyue)
            try:
                student.meal_balance = wucanyue
                student.remaining_hours = keshiyue
                student.save()
                new_Record = StudentRecord(student_name=student_name, file_number=studentid, changed_hours=-koujian,
                                           remaining_hours=keshiyue, deducted_meal_fee=-wucan, meal_balance=wucanyue,
                                           morning=moring, afternoon=afternoon, lunch=lunch, note=note, oc_time=oc_time
                                           ,tag="更新")
                new_Record.save()
                return JsonResponse({'status': 'success', 'message': '写入数据库成功'})
            except Exception as e:
                print(f'Error: {e}')
                return JsonResponse({'message': 'Error occurred while sending koujian notification'}, status=500)
        else:
            return JsonResponse({'message': 'Error occurred while sending koujian notification'}, status=500)


class send_qiandao(APIView):
    """
    发送扣减通知
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'qiandao.html')

    def post(self, request, *args, **kwargs):
        oc_time = request.data['time22']['value']
        try:
            for iss in request.data["students"]:
                studentid = iss['studentId']
                student_name = iss['name']
                file_number = iss['studentId']
                note = iss['beizhu']
                moring = False
                afternoon = False
                lunch = False
                studentprofile = StudentProfile.objects.get(archive_number=studentid)
                keshiyue = iss['keshiyue']
                wucanyue = iss['canfeiyue']
                koujian = 0
                wucan = 0
                if '上午' in iss['checkedTimes']:
                    koujian = koujian + 1
                    moring = True
                if '下午' in iss['checkedTimes']:
                    koujian = koujian + 1
                    afternoon = True
                if '午餐' in iss['checkedTimes']:
                    wucan = wucan + 10
                    lunch = True
                # 更新主表餐费余额及课时余额
                keshiyue = keshiyue - koujian
                wucanyue = Decimal(wucanyue) - wucan
                studentprofile.meal_balance = wucanyue
                studentprofile.remaining_hours = keshiyue
                studentprofile.save()
                # 新增签到行
                new_Record = StudentRecord(student_name=student_name, file_number=file_number, changed_hours=-koujian,
                                           remaining_hours=keshiyue, deducted_meal_fee=-wucan, meal_balance=wucanyue,
                                           morning=moring, afternoon=afternoon, lunch=lunch, note=note, oc_time=oc_time,
                                           tag="签到")
                new_Record.save()
            return JsonResponse({'status': 'success', 'message': '写入数据库成功'})
        except Exception as e:
            ss = str(e)
        return JsonResponse({'status': 'error', 'message': ss})


class qiandao_list(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'qiandaolist.html')


class get_qiandao_list(APIView):
    def get(self, request, *args, **kwargs):
        studenrecords = StudentRecord.objects.all()
        stujs = {
            "records":[]
        }


        for stu in studenrecords:
            i = 0
            checkdTitles = []
            if stu.morning:
                checkdTitles.append("上午")
            if  stu.afternoon:
                checkdTitles.append("下午")
            if stu.lunch:
                checkdTitles.append("午餐")
            student_data = {
                "studentId": stu.file_number,
                "name": stu.student_name,
                "keshiyue": stu.remaining_hours,
                "canfeiyue": stu.meal_balance,
                "change_hours": stu.changed_hours,
                "bencicanfei": stu.deducted_meal_fee,
                # "morning": stu.morning,
                # "afternoon": stu.afternoon,
                # "lunch": stu.lunch,
                "tag":stu.tag,
                "oc_time": stu.oc_time.strftime("%Y-%m-%d"),
                "checkedTimes": checkdTitles,
                "beizhu": stu.note,
            }
            stujs['records'].append(student_data)

        return JsonResponse(stujs)

class chongzhi(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'chongzhi.html')

    def post(self, request, *args, **kwargs):
        print(request.data)
        student_name = request.data['student_name']['name']
        file_number = request.data['student_name']['value']
        recharge_date = request.data['recharge_date']
        recharge_hours = request.data['recharge_hours']
        recharge_meal_fee = request.data['recharge_meal_fee']
        note = request.data['note']
        if request.data['radioValue']==1:
            payment_method = '现金'
        elif request.data['radioValue']==2:
            payment_method = '微信'
        elif request.data['radioValue']==3:
            payment_method = '转账'
        else:
            payment_method = '其他'
        try:
            # 新增签到行
            new_Record = RechargeRecord(student_name=student_name,file_number=file_number,recharge_date=recharge_date,
                                        recharge_hours=recharge_hours,recharge_meal_fee=recharge_meal_fee,
                                        payment_method=payment_method, note=note)
            new_Record.save()
            studentprofile = StudentProfile.objects.filter(archive_number=file_number).last()
            studentprofile.remaining_hours = studentprofile.remaining_hours + Decimal(recharge_hours)
            studentprofile.meal_balance = studentprofile.meal_balance + Decimal(recharge_meal_fee)
            studentprofile.save()
            return JsonResponse({'status': 'success', 'message': '写入数据库成功'})
        except Exception as e:
            ss = str(e)
        return JsonResponse({'status': 'error', 'message': ss})

class Index(APIView):
    def get(self, request, *args, **kwargs):
        # //跳转index.html
        return render(request, 'index.html')