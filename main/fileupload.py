
from django.shortcuts import render

import pandas as pd 
#from django.db import connection
from .models import Fransa

def handle_uploaded_file(f , data):
    pd_file =pd.read_excel(f)
    print(pd_file)
    
    order_id_list = [a for a in pd_file['AmazonOrderId']]
    print(len(order_id_list))
    asin_list = [ a for a in pd_file['ASIN']]
    #cost_list = [a for a in pd_file['Cost(£)']]
    buyer_order_id_list= [a for a in pd_file['ShippingOrderId']]
    '''
    query = str(Data.objects.all().query)
    df = pd.read_sql_query(query, connection)
    pd_temp = df[["SATICI_SIPARIS_NUMARASI" , "TARIH" , 'SATIS_FIYATI' , 'AMAZON_FEE']]
    print(pd_temp)
    '''

    for x in data.objects.all():
     #  b = Data.objects.all().filter(SATICI_SIPARIS_NUMARASI = x)
        
        if x.SATICI_SIPARIS_NUMARASI in order_id_list :
            print(1)
            index = pd_file.index[pd_file['AmazonOrderId'] == str(x)].tolist()
            asin = asin_list[index[0]]
            buyer_order_id = buyer_order_id_list[index[0]]
            x.ALICI_SIPARIS_NUMARASI=buyer_order_id
            x.ASIN = asin
            x.save()
            print(asin)
        
            
            

            