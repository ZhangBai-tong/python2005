import random
import re

from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status, status
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.settings import api_settings

from edu_api.libs.geetest import GeetestLib
from edu_api.settings import constants
from edu_api.utils.send_msg import Message
from user.models import UserInfo
from user.serializer import UserModelSerializer
from user.service import get_user_by_account

pc_geetest_id = "759d5436a6bfe1e0a94d222e9452097b"
pc_geetest_key = "2061a99f3c25e50989a0c04536132953"


class CaptchaAPIView(APIView):
    """极验验证码"""

    user_id = 1
    status = False

    def get(self, request):
        """获取验证码"""
        username = request.query_params.get("username")
        print(31, username)
        user = get_user_by_account(username)
        print(33, user)
        if user is None:
            return Response({"message": "该用户不存在"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        # 通过极验类生成验证码对象
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request):
        """验证验证码"""

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge")
        validate = request.data.get("geetest_validate")
        seccode = request.data.get("geetest_seccode")
        # 判断用户是否存在
        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        print(58, result)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


class UserAPIView(CreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


class SendMessageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        redis_connection = get_redis_connection('sms_code')
        # 判断手机号在60秒内是否发送过短信
        phone = request.query_params.get('phone')
        print(phone, 9999)
        phone_code = redis_connection.get('sms_%s' % phone)
        if phone_code is not None:
            return Response({'message': "60秒内已经发送过了，别瞎搞~"}, status=http_status.HTTP_400_BAD_REQUEST)

        # 2. 生成随机的短信验证码
        code = random.randint(100000, 999999)

        # 3. 将验证码保存至redis
        redis_connection.setex("sms_%s" % phone, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex("mobile_%s" % phone, constants.PHONE_EXPIRE_TIME, code)

        # 4. 调用方法  完成短信的发送
        try:
            msg = Message(constants.API_KEY)
            print(code)
            msg.send_message(phone, code)
        except:
            return Response({"message": "短信发送失败"}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5. 将发送的结果响应回去
        return Response({"message": "短信发送成功"}, status=http_status.HTTP_200_OK)


class CheckPhoneNumber(ModelViewSet):
    """注册判断手机号"""

    def check_phone(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        # 验证手机号唯一性
        phone1 = UserInfo.objects.filter(phone=phone)
        if phone1:
            return Response({'message': '手机号已被注册，请换手机号'}, status=status.HTTP_400_BAD_REQUEST)
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return Response({'message': '手机号格式有误，请重新输入！'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'OK', }, status=http_status.HTTP_200_OK)


class LoginSMSAPIVIew(ModelViewSet):
    def check_phone_login(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        print(11, phone, type(phone))
        m_phone = UserInfo.objects.filter(phone=phone)
        # 验证手机号格式
        # if not re.match(r'^1[3-9]\d{9}$', phone):
        #     return Response({'message': '手机号格式有误，请重新输入！'}, status=status.HTTP_400_BAD_REQUEST)
        if m_phone:
            return Response({'message': '登录成功'}, status=status.HTTP_200_OK)
        return Response({'message': '手机号未被注册，请注册后登录'}, status=status.HTTP_400_BAD_REQUEST)


# class codeSMSAPIVIew(ModelViewSet):
#     def check_code_login(self, request, *args, **kwargs):
#         sms_code = request.data.get('sms_code')
#         print(11, sms_code, type(sms_code))
#         code1 = UserInfo.objects.filter(sms_code=sms_code)
#         if code1:
#             return Response({'message': '登录成功'}, status=status.HTTP_200_OK)
#         return Response({'message': '验证码错误，请输入正确验证码'}, status=status.HTTP_400_BAD_REQUEST)


class MessageModel(ModelViewSet):
    """短信登录"""

    def login_message(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        code = request.data.get('sms_code')
        print(code)
        user = UserInfo.objects.filter(phone=phone).first()
        # 获取redis链接
        conn = get_redis_connection('sms_code')
        phone_code = conn.get('mobile_%s' % phone)
        phone_code = phone_code.decode('utf-8')
        if code != phone_code or code == "":
            return Response({'message': "验证码错误"}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 根据用户生成载荷
            payload = jwt_payload_handler(user)
            # 根据载荷生成token
            user.token = jwt_encode_handler(payload)
            print(UserModelSerializer(user).data, 165)
            return Response({
                'message': '登陆成功',
                'data': UserModelSerializer(user).data
            }, status=http_status.HTTP_200_OK)
        return Response({
            'message': '登陆失败，手机号没有被注册',
        }, status=http_status.HTTP_400_BAD_REQUEST)
