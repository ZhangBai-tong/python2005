from rest_framework.serializers import ModelSerializer
from course.models import CourseCategory, Course, Teacher, CourseLesson, CourseChapter


class CourseCategoryModelSerializer(ModelSerializer):
    """课程分类"""

    class Meta:
        model = CourseCategory
        fields = ("id", "name")


class TeacherModelSerializer(ModelSerializer):
    """讲师"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "title", "role", "signature", "image", "brief")


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list", "discount_name", "discount_price")


class CourseDetailModelSerializer(ModelSerializer):
    """课程详细信息的序列化器"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "level_name", "brief_html",
                  "discount_name", "discount_price", "active_time")


class CourseLessonModelSerializer(ModelSerializer):
    """课程课时"""

    class Meta:
        model = CourseLesson
        fields = ("id", "name", "duration", "free_trail")


class CourseChapterModelSerializer(ModelSerializer):
    """课程章节"""
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ("id", "name", "coursesections", "chapter")
