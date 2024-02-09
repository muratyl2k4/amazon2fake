from .models import Order
import pandas as pd 

from .courier_code import courier_code
from operator import countOf
def common_member(a, b):
    result = [i for i in a if countOf(b,i)>0]
    return result

def uploaded_file(file , data):
    pd_file = pd.read_excel(file)
    pd_file = pd_file.where(pd.notnull(pd_file), None)
    ## excel kolonlarini listeye cevirme
    carrier = [x for x in pd_file['Carrier']]
    trackingID = [x for x in pd_file['Tracking ID']]
    fileAmazonOrderId = [x for x in pd_file['AmazonOrderId']]
    dbAmazonOrderId = [x.get('SATICI_SIPARIS_NUMARASI') for x in data.objects.values()]
    ## veritabanindaki ve yuklenen dosyadaki eslesen order idleri alma
    common_tracks = common_member(fileAmazonOrderId , dbAmazonOrderId)
    for i in common_tracks:
        index = pd_file.index[pd_file['AmazonOrderId'] == i].tolist()
        #varsa ekleme yoksa olusturma
        try: 
            track = Order.objects.get(AmazonOrderId= fileAmazonOrderId[index[0]])
            if track.Tracknumber == None: track.Tracknumber = trackingID[index[0]] if trackingID[index[0]] is not None else None
            if track.Tracknumber2 == None and track.Tracknumber != trackingID[index[0]] : track.Tracknumber2 = trackingID[index[0]] if trackingID[index[0]] is not None else None
            if track.Courier_Name == None or track.Courier_Name != courier_code(carrier[index[0]]): track.Courier_Name = courier_code(carrier[index[0]]) if carrier[index[0]] is not None else None              
            track.save()            
        except Order.DoesNotExist:
            track = Order(
            AmazonOrderId  = fileAmazonOrderId[index[0]] , 
            Tracknumber = trackingID[index[0]] if trackingID[index[0]] is not None else None , 
            Courier_Name = courier_code(carrier[index[0]]) if carrier[index[0]] is not None else None 
            )
            track.save()
        

    
