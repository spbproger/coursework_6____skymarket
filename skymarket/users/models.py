from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from .managers import UserManager, UserRoles
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser):
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role']

    first_name = models.CharField(max_length=100, verbose_name="Имя", null=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", null=True)
    phone = PhoneNumberField(verbose_name="Телефон")
    email = models.EmailField(verbose_name="email address", unique=True, max_length=50)
    role = models.CharField(max_length=5, verbose_name="Роль пользователя", choices=UserRoles.choices,
                            default=UserRoles.USER)
    image = models.ImageField(upload_to='users/', verbose_name="Фото пользователя", null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Активность аккаунта", null=True, default=True)

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.email