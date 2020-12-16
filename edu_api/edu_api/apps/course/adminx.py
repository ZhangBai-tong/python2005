import xadmin

from course import models
from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryAdmin(object):
    """课程分类表"""
    list_display = ["name"]


xadmin.site.register(CourseCategory, CourseCategoryAdmin)


class CourseAdmin(object):
    """课程信息表"""
    list_display = ["name", "status",
                    "course_category", "lessons", "pub_lessons",
                    "price", "teacher"]


xadmin.site.register(Course, CourseAdmin)


class TeacherAdmin(object):
    """讲师表"""
    list_display = ["name", "role", "title", "signature", "image", "brief"]


xadmin.site.register(Teacher, TeacherAdmin)


class CourseChapterAdmin(object):
    """章节表"""
    list_display = ["course", "chapter", "name", "summary", "pub_date"]


xadmin.site.register(CourseChapter, CourseChapterAdmin)


class CourseLessonAdmin(object):
    """课时表"""
    list_display = ["name", "section_type", "section_link", "duration", "pub_date", "course", "is_show_list"]


xadmin.site.register(CourseLesson, CourseLessonAdmin)


class CourseDiscountAdmin(object):
    """课程折扣模型"""
    list_display = ["discount_type", "condition", "sale"]


xadmin.site.register(models.CourseDiscount, CourseDiscountAdmin)


class CourseDiscountTypeAdmin(object):
    """课程优惠类型模型"""
    list_display = ["name", "remark"]


xadmin.site.register(models.CourseDiscountType, CourseDiscountTypeAdmin)


class ActivityAdmin(object):
    """课程优惠时间表"""
    list_display = ["name", "start_time", "end_time", "remark"]


xadmin.site.register(models.Activity, ActivityAdmin)


class CoursePriceDiscountAdmin(object):
    """课程与价格策略关系表"""
    pass


xadmin.site.register(models.CoursePriceDiscount, CoursePriceDiscountAdmin)


class CourseExpireAdmin(object):
    """课程与价格策略关系表"""
    pass


xadmin.site.register(models.CourseExpire, CourseExpireAdmin)
