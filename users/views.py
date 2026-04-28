from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.serializers import (PaymentSerializer, UserCreateSerializer, UserSerializer)
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания платежа через Stripe"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # Определяем имя продукта (курс, урок или общая оплата)
        product_name = "Оплата обучения"
        if payment.paid_course:
            product_name = payment.paid_course.title
        elif payment.paid_lesson:
            product_name = payment.paid_lesson.title

        # Магия Stripe
        stripe_product_id = create_stripe_product(product_name)
        stripe_price = create_stripe_price(payment.amount, stripe_product_id)
        payment_link, session_id = create_stripe_session(stripe_price.id)

        # Сохраняем полученные данные в базу
        payment.link = payment_link
        payment.session_id = session_id
        payment.save()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]