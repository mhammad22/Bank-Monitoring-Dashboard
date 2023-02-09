# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import BankDetailsView, EachBankDetailsView, RefreshTimeView

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('bank-details/', BankDetailsView.as_view(), name='bank-details'),
    path('bank-details/<str:parameter>/', EachBankDetailsView.as_view(), name='each_bank_detail'),
    path('refresh-time/', RefreshTimeView.as_view(), name='refresh-time'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
