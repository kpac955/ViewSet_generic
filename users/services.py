import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Создает продукт в Stripe."""
    try:
        product = stripe.Product.create(name=name)
        return product.id
    except stripe.error.StripeError as e:
        print(f"Ошибка Stripe при создании продукта: {e}")
        return None


def create_stripe_price(amount, product_id):
    """Создает цену в Stripe (сумма переводится в копейки)."""
    if amount <= 0:
        raise ValueError("Сумма оплаты должна быть больше нуля.")

    try:
        price = stripe.Price.create(
            currency="rub",
            unit_amount=int(amount * 100),
            product=product_id,
        )
        return price
    except stripe.error.StripeError as e:
        print(f"Ошибка Stripe при создании цены: {e}")
        return None


def create_stripe_session(price_id):
    """Создает сессию оплаты и возвращает ссылку и ID сессии."""
    try:
        session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/",
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
        )
        return session.url, session.id
    except stripe.error.StripeError as e:
        print(f"Ошибка Stripe при создании сессии: {e}")
        return None, None


def get_stripe_session_status(session_id):
    """
    Получает данные сессии из Stripe для проверки статуса.
    Нужно для выполнения пункта о проверке статуса платежа.
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status
    except stripe.error.StripeError as e:
        print(f"Ошибка Stripe при получении сессии: {e}")
        return None
