from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.serializers import (PaymentSerializer, UserCreateSerializer,
                               UserSerializer)
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session, get_stripe_session_status)


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

    @extend_schema(
        summary="Создание платежа через Stripe",
        description=(
            "Создает объект платежа, затем регистрирует продукт и цену в Stripe, "
            "генерирует сессию оплаты и возвращает ссылку. "
            "Сумма передается в копейках. Требуется авторизация."
        ),
        responses={
            201: PaymentSerializer,
            400: OpenApiResponse(description="Ошибка в данных (например, сумма <= 0)"),
            500: OpenApiResponse(description="Ошибка на стороне Stripe"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Сохраняем базу платежа
        payment = serializer.save(user=self.request.user)

        # 1. Определяем имя продукта (курс или урок)
        product_name = "Оплата обучения"
        if payment.paid_course:
            product_name = f"Курс: {payment.paid_course.title}"
        elif payment.paid_lesson:
            product_name = f"Урок: {payment.paid_lesson.title}"

        # 2. Интеграция со Stripe (с обработкой ошибок внутри сервиса)
        stripe_product_id = create_stripe_product(product_name)

        if stripe_product_id:
            stripe_price = create_stripe_price(payment.amount, stripe_product_id)

            if stripe_price:
                payment_link, session_id = create_stripe_session(stripe_price.id)

                # 3. Сохраняем ВСЕ данные в модель
                payment.product_id = stripe_product_id
                payment.price_id = stripe_price.id
                payment.session_id = session_id
                payment.link = payment_link
                # Статус по умолчанию 'created'
                payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для проверки статуса платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Детали платежа и проверка статуса",
        description=(
            "Возвращает данные платежа. Если у платежа есть session_id, "
            "контроллер обращается к Stripe, проверяет статус оплаты "
            "и обновляет его в базе данных (статус 'paid')."
        ),
    )
    def get(self, request, *args, **kwargs):
        payment = self.get_object()

        # Если сессия создана, но платеж еще не помечен как оплаченный в БД
        if payment.session_id and payment.status != "paid":
            stripe_status = get_stripe_session_status(payment.session_id)

            # Если Stripe подтверждает, что оплата прошла
            if stripe_status == "paid":
                payment.status = "paid"
                payment.save()

        return super().get(request, *args, **kwargs)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
