from django.shortcuts import render
from data_downloader.models import MarketingAuthorisation


def home(request):
    latest_marketing_authorisations = MarketingAuthorisation.objects.order_by('-record_date')
    context = {'latest_marketing_authorisations': latest_marketing_authorisations}
    return render(request, 'website/home.html', context)


def ma_overview(request):
    pass


def ma_detail(request, ma_number):
    pass


def company_overview(request):
    pass


def company_detail(request, company_id):
    pass
