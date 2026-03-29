from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_link


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[validate_youtube_link], required=False, allow_null=True
    )
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
            "owner",
        )

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на этот курс."""
        user = self.context.get("request").user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
