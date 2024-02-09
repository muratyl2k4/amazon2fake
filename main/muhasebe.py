from imap_tools import MailBox , AND
from .models import Almanya , Ingiltere , Fransa
import re
import locale
from bs4 import BeautifulSoup
from datetime import datetime


def mailparse(user , country , email , apppassword , fdate):
    print(fdate)
    if country == Almanya : 
        subjectFilter = 'Artikel verkauft - Bitte jetzt verschicken:'
        rOrderId = 'Bestellnummer:'
        rOrderDate = 'Verkauft am: '
        rPrice = 'Preis: '
        rShipping = 'Versandkosten: '
        rAmazonFee = 'Amazon-Gebühren: '
        rYourEarnings = 'Ihre Einnahmen: '
        rCurrency = 'EUR'
    if country == Ingiltere : 
        subjectFilter = 'Sold, dispatch now:'
        rOrderId = 'Order ID:'
        rOrderDate = 'Order date: '
        rPrice = 'Price: '
        rShipping = 'Shipping: '
        rAmazonFee = 'Amazon fees: '
        rYourEarnings = 'Your earnings: '
        rCurrency = '£'
    if country == Fransa:
        subjectFilter = f"Commande"
        rOrderId = 'Commande n° :'
        rOrderDate = 'Date de la vente : '
        rPrice = 'Prix : '
        rShipping = 'Shipping: '
        rAmazonFee = 'Frais Amazon.fr : '
        rYourEarnings = 'Montant total dû au vendeur : '
        rCurrency = 'EUR'

        


    ###EMAIL PARSE
    username = email
    app_password = apppassword
    mb = MailBox('imap.gmail.com').login(username, app_password)
    last_date = list(country.objects.filter(KULLANICI = user))
    dx = datetime.strptime(fdate , '%Y-%m-%d').date() if not fdate == None else None
    if len(last_date) > 0:
        dx = last_date[-1].TARIH
    
    messages = mb.fetch(AND(subject=subjectFilter , date_gte=dx))
    liste = []
    i=0 
     
    for msg in messages:
         
        i+=1
        
        
        if country == Ingiltere or country ==Fransa : mail = BeautifulSoup(msg.html , 'html.parser').prettify()
        elif country == Almanya : mail = msg.text

        ##FROM 
        #ORDER İD 
        order_id_text=re.findall(f"{rOrderId} .*$",mail,re.MULTILINE)
        for x in order_id_text:

            order_id = re.findall('(?<=: )(.*)', x)
            oi = order_id[0]

            
        #ORDER DATE
        order_date_text=re.findall(f"{rOrderDate}.*$",mail,re.MULTILINE)
        locale.setlocale(locale.LC_ALL, 'en_US')

        for x in order_date_text:
            order_date = re.findall('(?<=: )(.*)', x)
            od = order_date[0]
            
        try : 
            datetime_object = datetime.strptime(od.replace('.' , '/')[0:len(od)], "%d/%m/%Y") if not country == Almanya else datetime.strptime(od.replace('.' , '/')[0:len(od)-1], "%d/%m/%Y")
        except Exception as e : 
            pass        
        #PRICE
        price_text=re.findall(f"{rPrice}.*$",mail,re.MULTILINE)
        for x in price_text:
            price = re.findall('(?<=: )(.*)', x)
            prc = price[0]
        
        #SHIPPING
        shipping_text=re.findall(f"{rShipping}.*$",mail,re.MULTILINE)
        for x in shipping_text:
            shipping = re.findall('(?<=: )(.*)', x)
            shp = shipping[0]
        
        
        #AMAZON FEES
        fee_text=re.findall(f"{rAmazonFee}.*$",mail,re.MULTILINE)
        for x in fee_text:
            fee = re.findall('(?<=: )(.*)', x)
            afee = fee[0]
            if country == Almanya or country == Fransa: afee = afee.replace('(' , '').replace(')' , '')
 
        #YOUR EARNING
        earning_text=re.findall(f"{rYourEarnings}.*$",mail,re.MULTILINE)
        for x in earning_text:
            earning = re.findall('(?<=: )(.*)', x)
            ern = earning[0]
        try:
            b = country.objects.get(SATICI_SIPARIS_NUMARASI = oi[0:len(oi)])
            
        except:
            try :
                b = country(
                    KULLANICI = user, 
                    SATICI_SIPARIS_NUMARASI = oi[0:19],
                    SATIS_FIYATI  = float(prc.replace(f"{rCurrency}" , "").replace(',' , '.')[0:len(prc)-1]),
                    AMAZON_FEE  = float(afee.replace(f"{rCurrency}" , "").replace(',' , '.')[0:len(afee)-1]),
                    TARIH = datetime_object,
                    MALIYET = 0,
                    DEPO_MALIYET = 0
                )
                b.save()
            except Exception as e:
                print(e) 
            
        
        
        
            
    