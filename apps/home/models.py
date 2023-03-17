# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from apps.home.db import BankTypes, StatusChoices, TransactionTypes
from django.utils import timezone

# Create your models here.


class BaseModel(models.Model):
    """Provide default fields that are expectedly to be needed by almost all models"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class BankDetails(BaseModel):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=20, null=True, blank=True, default='MayBank')
    account_type = models.CharField(max_length=20, choices=BankTypes.choices,
                                    null=True, blank=True)
    account_num = models.DecimalField(max_digits=40, decimal_places=5, null=True, 
                                      blank=True)
    current_balance = models.DecimalField(max_digits=40, decimal_places=5, null=True,
                                 blank=True)
    available_balance = models.DecimalField(max_digits=40, decimal_places=5, null=True,
                                 blank=True)
    one_day_float = models.DecimalField(max_digits=40, decimal_places=5, null=True,
                                 blank=True)
    two_day_float = models.DecimalField(max_digits=40, decimal_places=5, null=True,
                                 blank=True)
    last_clearing = models.DecimalField(max_digits=40, decimal_places=5, null=True,
                                 blank=True)
    is_enabled = models.BooleanField(default=True, null=True)
    last_synced = models.DateTimeField(default=timezone.now,blank=True, null=True)
  
class AccountDetails(BaseModel):
    bank = models.ForeignKey(BankDetails, on_delete=models.CASCADE, db_index=True, related_name='bank_detail')
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=40, decimal_places=5, null=True, blank=True)
    trans_type = models.CharField(max_length=20, choices=TransactionTypes.choices, null=True, blank=True, default=TransactionTypes.DEBIT)
    balance = models.DecimalField(max_digits=40, decimal_places=5, null=True, blank=True)
    trans_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, null=True, blank=True, default=StatusChoices.TODO)
    
    class Meta:
        unique_together = ["trans_date", "description", "amount", "trans_type"]  
    

class TaskTime(BaseModel):
    time = models.DecimalField(max_digits=40, decimal_places=5, null=True, blank=True)