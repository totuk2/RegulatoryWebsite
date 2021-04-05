from django.contrib import admin
from .models import *


# Register your models here.
class RegRecord(admin.TabularInline):
    model = MarketingAuthorisation
    extra = 1


# class

admin.site.register(MarketingAuthorisation)
