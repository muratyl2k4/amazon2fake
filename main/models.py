from django.db import models

from django.db import models
from django.contrib.auth.models import User


###VERİTABANI MODELLERİ
class Data(models.Model):
    uuid = models.UUIDField( unique=True, editable=False , null=True , blank = True)
    KULLANICI = models.ForeignKey(User , blank=True , null=True , on_delete = models.CASCADE)
    
    TARIH = models.DateField(null=True , blank=True)
    ASIN = models.CharField(max_length=100 , null=True ,  blank=True)
    ALICI_SIPARIS_NUMARASI = models.CharField(max_length=100 , null=True,  blank=True)
    SATICI_SIPARIS_NUMARASI = models.CharField(max_length=100,null=True, blank=True)
    SATIS_FIYATI = models.FloatField(blank=True , null=True)
    AMAZON_FEE = models.FloatField(blank=True ,null=True)
    MALIYET = models.FloatField(blank=True , null=True)
    DEPO_MALIYET = models.FloatField(blank=True , null=True)
    KAR = models.FloatField(blank=True , null=True)
    YUZDELIK_KAR = models.FloatField(blank=True , null=True)
    class Meta:
        abstract = True
    def __str__(self):
        return self.SATICI_SIPARIS_NUMARASI

class Ingiltere(Data):
    def __init__(self, *args, **kwargs):
        for f in self._meta.fields:
            if f.attname == "parent_field":
                f.default = "child default"
        super(Ingiltere, self).__init__(*args, **kwargs)
class Almanya(Data):
    def __init__(self, *args, **kwargs):
        for f in self._meta.fields:
            if f.attname == "parent_field":
                f.default = "child default"
        super(Almanya, self).__init__(*args, **kwargs)
class Fransa(Data):
    def __init__(self, *args, **kwargs):
        for f in self._meta.fields:
            if f.attname == "parent_field":
                f.default = "child default"
        super(Fransa, self).__init__(*args, **kwargs)
class Pazarlar(models.Model):
    KULLANICI = models.ForeignKey(User , blank=True , null=True , on_delete = models.CASCADE)
    UK = models.BooleanField(null=True , blank=True)
    UKMAIL = models.CharField(null=True , blank=True , max_length=250)
    UKPASSWORD = models.CharField(null=True , blank=True , max_length=250)

    FR = models.BooleanField(null=True , blank=True)
    FRMAIL = models.CharField(null=True , blank=True , max_length=250)
    FRPASSWORD = models.CharField(null=True , blank=True , max_length=250)
    
    DE = models.BooleanField(null=True , blank=True)
    DEMAIL = models.CharField(null=True , blank=True , max_length=250)
    DEPASSWORD = models.CharField(null=True , blank=True , max_length=250)
    def get_items(self , ukKazanc , ukProfit ,ukMaliyet ,frKazanc ,frProfit , frMaliyet , deKazanc , deProfit , deMaliyet):

        items = [('UK' , self.UK , '../ingiltere' , ukKazanc , ukProfit , ukMaliyet , 'İNGİLTERE') 
                 ,('FR' , self.FR , '../fransa' , frKazanc , frProfit , frMaliyet , 'FRANSA') ,
                   ('DE' , self.DE , '../almanya' , deKazanc, deProfit , deMaliyet , 'ALMANYA')]
        return items



    
class excelData(models.Model):
    file = models.FileField(upload_to='attachment/%Y/%m/%d')
