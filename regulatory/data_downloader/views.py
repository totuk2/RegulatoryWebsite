from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from .static.data_downloader.pl_XMLParser_2 import download_and_parse


# Create your views here.
def IndexView(request):
    return render(
        request,
        'data_downloader/index.html',
        context={}
    )


def UpdateDBView(request):
    data_list = download_and_parse()
    for record in data_list:
        try:
            inn_name, inn_created = INN_Name.objects.get_or_create(inn_name=record.pop('inn_name'))
        except KeyError:
            inn_name, inn_created = INN_Name.objects.get_or_create(inn_name='unknown')
        try:
            ma_holder, mah_created = Company.objects.get_or_create(ma_holder=record.pop('ma_holder'))
        except KeyError:
            ma_holder, mah_created = Company.objects.get_or_create(ma_holder='unknown')
        try:
            procedure_type, procedure_type_created = RegulatoryProcedure.objects.get_or_create(
                procedure_type=record.pop('procedure_type'))
        except KeyError:
            procedure_type, procedure_type_created = RegulatoryProcedure.objects.get_or_create(procedure_type='unknown')

        active_substances = []
        try:
            for api in record['active_substance']:
                active_substance, active_substances_created = ActivePharmaIngredient.objects.get_or_create(api_name=api)
                active_substances.append(active_substance)
                record.pop('active_substance', None)
        except KeyError:
            active_substances = []
            # record.pop('active_substance', None)

        r = MarketingAuthorisation.objects.create(
            inn_name=INN_Name.objects.get(inn_name=inn_name),
            ma_holder=Company.objects.get(ma_holder=ma_holder),
            procedure_type=RegulatoryProcedure.objects.get(procedure_type=procedure_type),
            # active_substance=ActivePharmaIngredient.objects.get(api_name=active_substances),
            **record
        )
        r.active_substance.set(active_substances)

    return render(request, 'data_downloader/update.html')
