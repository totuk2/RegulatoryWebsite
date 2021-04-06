from bs4 import BeautifulSoup as Soup
from django.core.management.base import BaseCommand, CommandError
from .models import *
import requests



db_field_mapper = {
    'stanNaDzien': 'record_date',
    'nazwaProduktu': 'product_name',
    'rodzajPreparatu': 'product_type',
    'nazwaPowszechnieStosowana': 'inn_name',
    'moc': 'strength',
    'postac': 'pharmaceutical_form',
    'podmiotOdpowiedzialny': 'ma_holder',
    'typProcedury': 'procedure_type',
    'numerPozwolenia': 'ma_number',
    'waznoscPozwolenia': 'ma_validity',
    'kodATC': 'atc_code1',
    'id': 'id_prod',
    'status': 'status',
    'wielkosc': 'pack_size',
    'jednostkaWielkosci': 'unit',
    'kodEAN': 'ean_14',
    'kategoriaDostepnosci': 'availability_cat',
    'skasowane': 'canceled',
    'numerEu': 'eu_number',
    'dystrybutorRownolegly': 'paralell_importer',
    'id_pack': 'id_pack',
    'substancjaCzynna': 'active_substance',
}

def download_and_parse():
    reg_incr_url = "http://pub.rejestrymedyczne.csioz.gov.pl/pobieranie_WS/Pobieranie.ashx?" \
                   "filetype=XMLUpdateFile&regtype=RPL_FILES_GROWTH"
    reg_incr_data = requests.get(reg_incr_url)

    if reg_incr_data.status_code == 200:
        handler = reg_incr_data.text

        #
        # def download_and_parse():
        #     handler = open("C:/Users/Piotr/PycharmProjects/reg2.xml").read()
        soup = Soup(handler, 'xml')
        records_list = []

        for product in soup('produktLeczniczy'):
            if product['rodzajPreparatu'] == 'ludzki':
                for opakowanie in product.find_all('opakowanie'):
                    # dopisz atrybuty opakowania
                    record = opakowanie.attrs
                    record['id_pack'] = record.pop('id')
                    # dopisz substancje czynna
                    api_list = []
                    for api in product.find_all('substancjaCzynna'):
                        api_list.append(api.string)
                        record.update({product.substancjaCzynna.name: api_list})
                    # dopisz date
                    record.update({'stanNaDzien': soup.produktyLecznicze.get('stanNaDzien')})
                    # Dopisz atrybuty produktu
                    for attrib in product.attrs:
                        record.update({attrib: product[attrib] for attrib in product.attrs})

                    record = {db_field_mapper[name]: val for name, val in record.items()}
                    records_list.append(record)
        return records_list

    # for product in download_and_parse():
    #     print(product.get('product_name'))

class Command(BaseCommand):
    def handle(self):
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

            self.stdout.write(self.style.SUCCESS('Successfully updated PL'))

