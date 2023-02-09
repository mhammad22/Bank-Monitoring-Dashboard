
from django.db.models.enums import TextChoices

class BankTypes(TextChoices):
    SAVING = 'SA', 'Saving Account'
    CURRENT = 'CA', 'Current Account'