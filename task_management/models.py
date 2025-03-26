from django.db import models
from django.contrib.auth.models import AbstractUser ,BaseUserManager

class CustomUserManager(BaseUserManager):
    """ Custom user manager without username field """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
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
    name = models.CharField(max_length=30, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)  
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # Avoids conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",  # Avoids conflict
        blank=True,
    )
    objects = CustomUserManager()
    USERNAME_FIELD = "email"  # Make email the unique identifier
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.name
    
class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    TASK_TYPE_CHOICES = (
        ('feature', 'Feature'),
        ('bug', 'Bug'),
        ('documentation', 'Documentation'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    
    def __str__(self):
        return self.name

