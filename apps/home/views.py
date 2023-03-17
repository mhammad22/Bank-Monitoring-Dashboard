# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from json import load
from django import template
from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.views import View
from datetime import datetime
from apps.home.forms import AddBankForm, RefreshTimeForm
from apps.home.models import BankDetails, AccountDetails, TaskTime
from apps.home.db import BankTypes
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'} 
    html_template = loader.get_template('home/index.html')
    
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    user = request.GET.get('user', '')
    bank_name = request.GET.get('bank', '')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()    
    
    
    # BankDetails.objects.create(
    #     username = 'shift1226',
    #     password = 'Hello5211!',
    #     url = 'https://www.maybank2u.com.my/home/m2u/common/login.do'
    # )
    # TaskTime.objects.create(
    #     time=1
    # )
    bank = BankDetails.objects.all().first()
    
    if start_date and end_date and user and bank:
        transactions = AccountDetails.objects.filter(
            Q(trans_date__range=[start_date, end_date]), 
            bank__name = bank_name,
            bank__username = user
        )
    else:
        transactions = AccountDetails.objects.all()
                                                 
    context = {
        'available_balance': BankDetails.objects.aggregate(Sum('available_balance'))['available_balance__sum'],
        'current_balance': BankDetails.objects.aggregate(Sum('current_balance'))['current_balance__sum'],
        'one_day_float': BankDetails.objects.aggregate(Sum('one_day_float'))['one_day_float__sum'],
        'two_day_float': BankDetails.objects.aggregate(Sum('two_day_float'))['two_day_float__sum'],
        'transactions': transactions,
        'banks': BankDetails.objects.all()
    }
    
    #get the list of all account transactions
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# Add bank detail to the db
@method_decorator(login_required, name='dispatch')
class BankDetailsView(View):
    template_name = 'home/bank_details.html'
    
    def get(self, request, *args, **kwargs):
        
        banks = BankDetails.objects.all()
        template_data = {
            'banks': banks,
            'form': AddBankForm(),
            'refresh_time': TaskTime.objects.all().first().time
        }
        return TemplateResponse(request, self.template_name, template_data)
    
    
    def post(self, request):
        form = AddBankForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            url = request.POST['url']
            BankDetails.objects.create(username=username, password=password, url=url)
        return redirect('bank-details')

# Refresh time view to set the refresh time
@method_decorator(login_required, name='dispatch')
class RefreshTimeView(View):
    template_name = 'home/refresh_time.html'
    
    def get(self, request, *args, **kwargs):
        
        template_data = {
            'form': RefreshTimeForm()
        }
        return TemplateResponse(request, self.template_name, template_data)
    
    
    def post(self, request):
        form = RefreshTimeForm(request.POST)
        if form.is_valid():
            time = request.POST['time']
            TaskTime.objects.all().delete()
            TaskTime.objects.create(time=time)
        return redirect('bank-details')
    

# View for each bank details under the Dashboard category 
@method_decorator(login_required, name='dispatch')
class EachBankDetailsView(View):
    template_name = 'home/index.html'
    
    def get(self, request, parameter):
        
        username = parameter
        bank = BankDetails.objects.filter(username=username).first()
        transactions = bank.bank_detail.all()
        template_data = {
            'available_balance': bank.available_balance,
            'current_balance': bank.current_balance,
            'one_day_float': bank.one_day_float,
            'two_day_float': bank.two_day_float,
            'transactions': transactions,
            'banks': BankDetails.objects.all()
        }
        return TemplateResponse(request, self.template_name, template_data)