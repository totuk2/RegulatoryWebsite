from bs4 import BeautifulSoup as Soup
from .field_mapping import db_field_mapper
import requests


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
