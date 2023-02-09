# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.apps import AppConfig


class MyConfig(AppConfig):
    name = 'apps.home'
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'apps_home'
