
from django.db.models.enums import TextChoices

class BankTypes(TextChoices):
    SAVING = 'SA', 'Saving Account'
    CURRENT = 'CA', 'Current Account'
    
class StatusChoices(TextChoices):
    TODO = 'TD', 'TODO'
    IN_PROGRESS = 'IP', 'In Progress'
    DONE = 'DN', 'Done'
    
class TransactionTypes(TextChoices):
    CREDIT = 'CD', 'Credit'
    DEBIT = 'DB', 'Debit'