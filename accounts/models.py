from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	"""Default user model with email as unique identifier."""

	email = models.EmailField('email address', unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
