from django.db import models
from django.contrib.auth.models import AbstractUser
from djangochamba.models import SoftDeleteModel
import uuid
from djangochamba.utils import generate_jti
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser, SoftDeleteModel):

    class Meta:
        default_permissions = () 

    # Types of users
    USER_ADMIN       = 1
    USER_PROFESSOR   = 2
    USER_STUDENT     = 3

    PASSWORD_PATTERN = '^(?=^.{8,}$)(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&*¿?¡!\'"ºª~€¬/(){}=+_\\-.,;:]).*$'
    EMAIL_PATTERN = '[^@]+@[^@]+\\.[^@]+'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    username = None
    current_session_id = models.IntegerField(blank=True, default=None, null=True)
    email              = models.EmailField(max_length=30, blank=False, unique=True)
    password_token     = models.CharField(max_length=20)
    uuid               = models.UUIDField(default=uuid.uuid4, unique=True)
    user_type          = models.PositiveSmallIntegerField(blank=False, default=USER_STUDENT)
    status             = models.BooleanField(default=True)
    second_last_name   = models.CharField(max_length=30, blank=False)
    control_number     = models.IntegerField(blank=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'
    )
    
    jwt_id = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        editable=False,
        default=generate_jti,
        help_text=_(u"JWT tokens for the user get revoked when JWT id has regenerated"),
    )

    def is_admin(self):
        return self.is_superuser
    
class UserSession(SoftDeleteModel):
    class Meta:
        default_permissions = ()
        verbose_name_plural = 'sesiones'
        verbose_name = 'sesión'

    login_date = models.DateTimeField(auto_now_add=True, blank=False, null=False, help_text=_(u'Login date'))
    logout_date = models.DateTimeField(blank=True, null=True, help_text=_(u'Logout date'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
