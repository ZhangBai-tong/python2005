from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    # 登录
    path("login/", obtain_jwt_token),
    # 注册
    path("sign_in/", views.UserAPIView.as_view()),
    # 滑块验证码
    path("message/", views.SendMessageAPIView.as_view()),
    # 点击登录按钮时 获取滑块验证码的url
    path("captcha/", views.CaptchaAPIView.as_view()),
    # 注册时判断手机号
    path("check_phone/", views.CheckPhoneNumber.as_view({'post': 'check_phone'})),
    path("check_phone_login/", views.LoginSMSAPIVIew.as_view({'post': 'check_phone_login'})),
    # path("check_code_login/", views.codeSMSAPIVIew.as_view({'post': 'check_code_login'})),
    # 短信登陆按钮
    path("login_message/", views.MessageModel.as_view({'post': 'login_message'})),
]
