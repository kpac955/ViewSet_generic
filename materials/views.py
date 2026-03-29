from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPaginator
from materials.permissions import IsModer, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с курсами."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.groups.filter(name="moderators").exists():
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionAPIView(APIView):
    """Управление подпиской на курсы."""

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока."""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Вывод списка уроков с пагинацией."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.groups.filter(name="moderators").exists():
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
