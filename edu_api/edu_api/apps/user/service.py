# 定义jwt的返回值
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "username": user.username,
        "user_id": user.id
    }


def get_user_by_account(account):
    try:
        # 根据用户输入的信息  判断用户输入的是手机号还是用户名或邮箱
        user = UserInfo.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
        print(user)
    except UserInfo.DoesNotExist:
        return None
    else:
        return user


class UserAuthentication(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        根据账号来获取用户对象
        :param request:    请求对象
        :param username:    前端输入的登录条件 手机号 用户名 邮箱
        :param password: 密码
        :return: 查询出的用户
        """

        # 1. 先判断输入类型  再进行查询
        user = get_user_by_account(username)
        # 2. 校验
        if user and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None
