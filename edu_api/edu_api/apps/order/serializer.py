from datetime import datetime

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# Create your views here.
from course.models import CourseExpire, Course
from order.models import Order, OrderDetail


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_number', 'pay_type')
        extra_kwargs = {
            'id': {'read_only': True},
            'order_number': {
                'read_only': True
            },
            'pay_type': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        pay_type = attrs.get('pay_type')
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError("你选择的支付方式不对")
        return attrs

    def create(self, validated_data):
        """生成订单 订单详情"""
        redis_connection = get_redis_connection('cart')

        user_id = self.context['request'].user.id
        incr = redis_connection.incr('number')

        # 生成唯一的订单号 时间戳+用户id+随机字符串
        order_number = datetime.now().strftime('%Y%m%d%H%M%S') + '%06d' % user_id + '%06d' % incr

        with transaction.atomic():
            # 事物回滚点
            rollback_id = transaction.savepoint()

            # 生成订单
            order = Order.objects.create(
                order_title="xx教育在线课程订单",
                total_price=0,
                real_price=0,
                order_number=order_number,
                order_status=0,
                pay_type=validated_data.get('pay_type'),
                credit=0,
                coupon=0,
                order_desc="你会为了你做了这个决定而感到高兴",
                user_id=user_id,
            )

            # 到redis获取购物车信息
            redis = get_redis_connection("cart")

            # 勾选状态
            course_selects_set = redis.smembers("cart_selected_%s" % user_id)
            print(course_selects_set)

            # 购物车中商品课程列表
            cart_list = redis.hgetall("cart_%s" % user_id)

            # 通过购物车信息到数据中提取相关数据
            # 开启redis的管道操作[事务操作]
            pipeline = redis.pipeline()
            pipeline.multi()

            # 生成订单详情
            cart_list = redis_connection.hgetall("cart_%s" % user_id)
            select_list = redis_connection.smembers("selected_%s" % user_id)

            for course_id_byte, expire_id_byte in cart_list.items():
                course_id = int(course_id_byte)
                expire_id = int(expire_id_byte)

                if course_id_byte in select_list:

                    try:
                        # 获取到购物车中所有的课程信息
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                    except Course.DoesNotExist:
                        continue

                    # 如果有效期的id大于0，则需要通过有效期对应的价格来计算活动真实价  id不大于0则使用课程本身的原价
                    original_price = course.price
                    expire_text = "永久有效"

                    try:
                        if expire_id > 0:
                            course_expire = CourseExpire.objects.get(id=expire_id)
                            # 对应有效期的价格
                            original_price = course_expire.price
                            expire_text = course_expire.expire_text
                    except CourseExpire.DoesNotExist:
                        pass

                    # 根据已勾选的商品对应的有效期的价格来计算商品的最终价格
                    final_price = course.final_price(expire_id)

                    try:
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=original_price,
                            real_price=final_price,
                            discount_name=course.discount_name
                        )

                        # TODO 从购物车中移除已经加入订单的商品
                        pipeline.srem("cart_selected_%s" % user_id, course_id)
                        pipeline.hdel("cart_%s" % user_id, course_id)
                        # 提交redis的事务操作
                        pipeline.execute()
                    except:
                        """回滚事务"""
                        transaction.savepoint_rollback(rollback_id)
                        raise serializers.ValidationError("订单生成失败")

                    # 计算订单总价
                    order.total_price += float(original_price)
                    order.real_price += float(final_price)

                order.save()

                # TODO 将订单生成成功后课程从购物车移除
            return order
