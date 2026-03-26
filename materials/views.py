from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from materials.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с курсами."""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_queryset(self):
        """Фильтрация курсов: модератор видит всё, пользователь — только своё."""
        queryset = super().get_queryset()
        if not self.request.user.groups.filter(name='moderators').exists():
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        """Разграничение прав доступа для разных действий."""
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Автоматическая привязка владельца при создании курса."""
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер создания урока."""
    serializer_class = LessonSerializer
    # Создавать уроки модератор не может
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        """Привязка владельца к уроку."""
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Контроллер вывода списка уроков."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтрация уроков: модератор видит всё, пользователь — только своё."""
        queryset = super().get_queryset()
        if not self.request.user.groups.filter(name='moderators').exists():
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер детального просмотра урока."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер редактирования урока."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер удаления урока."""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
