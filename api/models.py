import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from pkg_resources import _
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .manager import UserManager


class CoreUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    create_ts = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(default='', blank=True, null=True, max_length=255)
    last_name = models.CharField(default='', blank=True, null=True, max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True, default='')
    email = models.EmailField(verbose_name='email_address', max_length=255, unique=True)
    phone = models.CharField(default='', null=True, blank=True, max_length=255)
    job_assigned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)
    is_valid =models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    has_restaurant = models.BooleanField(default=False)
    car_name = models.CharField(max_length=255, null=True, blank=True, default='')
    car_number = models.CharField(max_length=255, null=True, blank=True, default='')
    permissions = ArrayField(models.CharField(default='', max_length=255, blank=True, null=True),
                             null=True, blank=True, default=list)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # @property
    # def is_staff(self):
    #     return self.staff


    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        return self.is_active

    def has_module_perms(self, app_label):
        return self.is_active

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return dict(
            refresh=str(refresh),
            access=str(refresh.access_token)
        )


class Shop(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    seller_id = models.ForeignKey(CoreUser, related_name='seller_id', on_delete=models.CASCADE)
    location =models.CharField(default='', max_length=255 , null=True, blank=True)
    class Meta:
        db_table= "shop"
        verbose_name_plural = "shop_1"

    def __str__(self):
        return str(self.id)





