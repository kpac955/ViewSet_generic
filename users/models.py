from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер для создания пользователей без поля username"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", blank=True, null=True
    )
    city = models.CharField(max_length=100, verbose_name="Город", blank=True, null=True)
    avatar = models.ImageField(
        upload_to="users/", verbose_name="Аватар", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    METHOD_CHOICES = [
        ("cash", "наличные"),
        ("transfer", "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    paid_course = models.ForeignKey(
        "materials.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )

    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default="transfer",
        verbose_name="Способ оплаты",
    )

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_date})"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
