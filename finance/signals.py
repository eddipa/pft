from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import transaction

from .models import TransactionCategory, TransactionAccount

DEFAULT_CATEGORIES = [
    {"name": "Food", "description": "Expenses for food and groceries"},
    {"name": "Transport", "description": "Public transport, fuel, etc."},
    {"name": "Rent", "description": "Monthly house or apartment rent"},
    {"name": "Entertainment", "description": "Movies, games, hobbies"},
    {"name": "Savings", "description": "Money set aside or invested"},
]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
         # Make sure user is fully saved in DB before creating related objects
        def create_categories():
            for cat in DEFAULT_CATEGORIES:
                TransactionCategory.objects.create(
                    user=instance,
                    name=cat["name"],
                    description=cat["description"]
            )   

        transaction.on_commit(create_categories)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_account(sender, instance, created, **kwargs):
    if created:
        TransactionAccount.objects.create(
            user=instance,
            name="Default Account",
            description="Automatically created account",
            is_default=True
        )