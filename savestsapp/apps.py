from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class SavestsappConfig(AppConfig):
    name = 'savestsapp'

class MyAdminConfig(AdminConfig):
    default_site = 'savestsapp.admin.MyAdminSite'