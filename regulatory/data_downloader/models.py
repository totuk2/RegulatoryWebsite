from django.db import models

# Datatype lengths
booleanAsString = 3
bigIntAsString = 19
integerAsString = 10
limitedString = 255
changeTypeString = 13
dateAsString = 10


# Create your models here.
class Company(models.Model):
    ma_holder = models.TextField()

    def __str__(self):
        return self.ma_holder


class ActivePharmaIngredient(models.Model):
    api_name = models.TextField()

    def __str__(self):
        return self.api_name


class INN_Name(models.Model):
    inn_name = models.CharField(max_length=limitedString)

    def __str__(self):
        return self.inn_name


class RegulatoryProcedure(models.Model):
    procedure_type = models.CharField(max_length=limitedString)

    def __str__(self):
        return self.procedure_type


class MarketingAuthorisation(models.Model):
    ma_number = models.CharField(max_length=limitedString)  # numerPozwolenia
    active_substance = models.ManyToManyField(ActivePharmaIngredient)  # substancjeCzynne
    product_name = models.CharField(max_length=limitedString)  # nazwaProduktu
    product_type = models.CharField(max_length=limitedString)  # rodzajPreparatu
    inn_name = models.ForeignKey(INN_Name, null=True, on_delete=models.SET_NULL)  # nazwaPowszechnieStosowana
    strength = models.CharField(max_length=limitedString)  # moc
    pharmaceutical_form = models.CharField(max_length=limitedString)  # postac
    ma_holder = models.ForeignKey(Company, on_delete=models.CASCADE)  # podmiotOdpowiedzialny
    procedure_type = models.ForeignKey(RegulatoryProcedure, on_delete=models.CASCADE)  # typProcedury
    ma_validity = models.CharField(max_length=limitedString)  # waznoscPozwolenia
    atc_code1 = models.CharField(max_length=limitedString)  # kodATC1
    # atc_code2 = models.CharField(max_length=2)  # kodATC2
    # atc_code3 = models.CharField(max_length=1)  # kodATC3
    # atc_code4 = models.CharField(max_length=1)  # kodATC4
    # atc_code5 = models.CharField(max_length=2)  # kodATC5
    id_prod = models.CharField(max_length=bigIntAsString)  # id_prod
    status = models.CharField(max_length=changeTypeString)  # status
    pack_size = models.CharField(max_length=limitedString)  # opakowanie_wielkosc
    unit = models.CharField(max_length=limitedString)  # jednostkaWielkosci
    ean_14 = models.CharField(max_length=limitedString)  # kodEAN
    availability_cat = models.CharField(max_length=limitedString)  # kategoriaDostepnosci
    canceled = models.CharField(max_length=booleanAsString)  # skasowane
    eu_number = models.CharField(max_length=limitedString)  # numerEu
    paralell_importer = models.CharField(max_length=booleanAsString)  # dystrybutorRownolegly
    id_pack = models.CharField(max_length=bigIntAsString)  # id_pack
    record_date = models.DateField()  # stanNaDzien

    def __str__(self):
        return self.product_name
