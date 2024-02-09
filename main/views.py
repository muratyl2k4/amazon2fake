from django.shortcuts import render
from .muhasebe import mailparse
from .models import Ingiltere , Almanya , Fransa , Pazarlar
from .fileupload import handle_uploaded_file
from .forms import UploadFileForm
from .forms import MALIYET
import pandas as pd 
import sqlite3
from django.core.files import File
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from imap_tools import MailBox
from google_currency import convert
import json





def home(request):
    return render(request , 'index.html') 

@login_required(login_url='login')
def dbdownload(request , country):
    now = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
    
    connection = sqlite3.connect("amazon2/db.sqlite3")
    query = f"SELECT * FROM main_{country} where KULLANICI_ID = {request.user.id}"
    df = pd.read_sql(query, connection)
    filename= f"{country}_{now}.xlsx"
    df.to_excel(f'amazon2/main/static/{filename}')
     
    db_path = f'amazon2/main/static/{filename}'
    dbfile = File(open(db_path, "rb"))
    response = HttpResponse(dbfile)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = dbfile.size

    return response

@login_required(login_url='login')
def muhasebe(request):
    global eur_to_usd 
    global gbp_to_usd
    temp = json.loads(convert('eur','usd',100))
    eur_to_usd = float(temp['amount'])/100
    temp2 = json.loads(convert('gbp','usd',100))
    gbp_to_usd = float(temp2['amount'])/100
    
    pazarlar = Pazarlar.objects.get(KULLANICI = request.user)
    print(pazarlar)
    if request.method == 'POST':
        try :
            mb = MailBox('imap.gmail.com').login(request.POST['mail'], request.POST['apppassword']) 
            if request.POST['countries'] == 'DE':
                pazarlar.DE = True
                pazarlar.DEMAIL = request.POST['mail']
                pazarlar.DEPASSWORD = request.POST['apppassword']
                
                pazarlar.save()
            elif request.POST['countries'] == 'UK':
                pazarlar.UK = True
                pazarlar.UKMAIL = request.POST['mail']
                pazarlar.UKPASSWORD = request.POST['apppassword']
                pazarlar.save()
            elif request.POST['countries'] == 'FR':
                pazarlar.FR = True
                pazarlar.FRMAIL = request.POST['mail']
                pazarlar.FRPASSWORD = request.POST['apppassword']
                pazarlar.save()
            messages.success(request , "Kayıt başarı ile tamamlandı")
        except Exception as e: 
            messages.error(request , "Hatalı Bilgi Girişi !")
            print(e)
        
    
    #c = CurrencyConverter()
    #pdict = {'pazarlar' : pazarlar.EN}
    #keys = [i for i in pdict.keys()]
    fr = Fransa.objects.filter(KULLANICI = request.user)
    frSatis = sum([i.SATIS_FIYATI for i in fr])
    frFee = sum([i.AMAZON_FEE for i in fr])
    frProfit = sum([i.KAR for i in fr if i.KAR is not None])
    frAmazonMaliyet = sum([i.MALIYET for i in fr])
    frDepoMaliyet = sum([i.DEPO_MALIYET for i in fr])
    frMaliyet = 0
    #frAmazonMaliyet + convert('eur','usd',frDepoMaliyet)
    
    de = Almanya.objects.filter(KULLANICI = request.user)
    deSatis = sum([i.SATIS_FIYATI for i in de])
    deFee = sum([i.AMAZON_FEE for i in de])
    deProfit = sum([i.KAR for i in de if i.KAR is not None])
    deAmazonMaliyet = sum([i.MALIYET for i in de])
    deDepoMaliyet = sum([i.DEPO_MALIYET for i in de])
    deMaliyet = 0
    #deAmazonMaliyet + convert('eur','usd',deDepoMaliyet)
    
    uk = Ingiltere.objects.filter(KULLANICI = request.user)
    ukSatis = sum([i.SATIS_FIYATI for i in uk])
    ukFee = sum([i.AMAZON_FEE for i in uk])
    ukProfit = sum([i.KAR for i in uk if i.KAR is not None])
    ukAmazonMaliyet = sum([i.MALIYET for i in uk])
    ukDepoMaliyet = sum([i.DEPO_MALIYET for i in uk])
    ukMaliyet = 0
    #ukAmazonMaliyet + convert('gbp','usd',ukDepoMaliyet)


    

    return render(request , 'muhasebe.html', {'x' : pazarlar.get_items(frKazanc= frSatis - frFee , frProfit=frProfit , frMaliyet=  frMaliyet ,
                                                                        deKazanc= deSatis - deFee, deProfit= deProfit , deMaliyet=deMaliyet ,
                                                                         ukKazanc=  ukSatis - ukFee , ukProfit=ukProfit , ukMaliyet=ukMaliyet),
                                                })

@login_required(login_url='login')
def ingiltere(request):
   
    
    pazarlar = Pazarlar.objects.get(KULLANICI = request.user)
    b = Ingiltere.objects.filter(KULLANICI = request.user)    
    d = reversed(b)
    form = UploadFileForm(request.POST, request.FILES)
    maliyet_form = MALIYET(request.POST) 
    
    print("request", request.POST)
    data = {
            "info" : d ,
            'len' : len(b) ,
            "form" : form , 
            
            }
        
    if request.method == 'POST':

        if 'load_excel' in request.POST:
            print("load excel")
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'] , d)
                updated_d = Ingiltere.objects.filter(KULLANICI = request.user)
                data = {
                "info" : updated_d,
                'form' : form,
                }
        
        elif 'update_cost' in request.POST:
            print("update_cost")
            if maliyet_form.is_valid():
                p_cost = maliyet_form.data['product_cost']
                w_cost = maliyet_form.data['warehouse_cost']
                o_id = maliyet_form.data['order_id']
                try:
                    update_cost(Ingiltere,o_id, p_cost, w_cost)
                    update_profit(Ingiltere,o_id ,'GBP')
                    return HttpResponseRedirect('../ingiltere')
                
                except :
                    message = "Maliyet 0 Olamaz"
                    data = {
                    "info" : d,
                    'form' : form,
                    'message' : message
                    }

        elif 'update_order_list' in request.POST:
            if len(b) == 0 : 
                mailparse(country=Ingiltere,user = request.user , email=pazarlar.UKMAIL , apppassword=pazarlar.UKPASSWORD , fdate=request.POST['date'])
            else:
                mailparse(country=Ingiltere,user = request.user , email=pazarlar.UKMAIL , apppassword=pazarlar.UKPASSWORD , fdate=None)
            return HttpResponseRedirect('../ingiltere')

    else:
        print("no form posted")
        form = UploadFileForm()

    
    return render(request , 'ingiltere.html' , data) 
    

@login_required(login_url='login')
def almanya(request):
   
    pazarlar = Pazarlar.objects.get(KULLANICI = request.user)
    b = Almanya.objects.filter(KULLANICI = request.user)    
    d = reversed(b)

    form = UploadFileForm(request.POST, request.FILES)
    maliyet_form = MALIYET(request.POST) 
    
    print("request", request.POST)
    data = {
            "info" : d ,
            'len' : len(b),
            "form" : form , 
            }
        
    if request.method == 'POST':

        if 'load_excel' in request.POST:
            print("load excel")
            if form.is_valid():
                handle_uploaded_file(f = request.FILES['file'] , data=Almanya)
                updated_d = reversed(Almanya.objects.filter(KULLANICI = request.user))
                data = {
                "info" : updated_d,
                'form' : form,
                }
        
        elif 'update_cost' in request.POST:
            print("update_cost")
            if maliyet_form.is_valid():
                p_cost = maliyet_form.data['product_cost']
                w_cost = maliyet_form.data['warehouse_cost']
                o_id = maliyet_form.data['order_id']
 
            try :
                update_cost(Almanya,o_id, p_cost, w_cost)
                update_profit(Almanya,o_id , 'EUR')
                return HttpResponseRedirect('../almanya')

            except :                
                message = "Maliyet 0 Olamaz"
                data = {
                "info" : d,
                'form' : form,
                'message' : message
                }


        elif 'update_order_list' in request.POST:
            if len(b) == 0 : 
                mailparse(country=Almanya,user = request.user , email=pazarlar.FRMAIL , apppassword=pazarlar.FRPASSWORD , fdate=request.POST['date'])
            else:
                mailparse(country=Almanya,user = request.user , email=pazarlar.FRMAIL , apppassword=pazarlar.FRPASSWORD , fdate=None)
            
            return HttpResponseRedirect('../almanya')
    else:
        print("no form posted")
        form = UploadFileForm()

    
    return render(request , 'almanya.html' , data)

@login_required(login_url='login')
def fransa(request):
   
    pazarlar = Pazarlar.objects.get(KULLANICI = request.user)
    b = Fransa.objects.filter(KULLANICI = request.user)    
    d = reversed(b)

    form = UploadFileForm(request.POST, request.FILES)
    maliyet_form = MALIYET(request.POST) 
    
    print("request", request.POST)
    data = {
            "info" : d ,
            'len' : len(b),
            "form" : form , 
            }
        
    if request.method == 'POST':

        if 'load_excel' in request.POST:
            print("load excel")
            if form.is_valid():
                handle_uploaded_file(f = request.FILES['file'] , data=Fransa)
                updated_d = reversed(Fransa.objects.filter(KULLANICI = request.user))
                data = {
                "info" : updated_d,
                'form' : form,
                }
        
        elif 'update_cost' in request.POST:
            print("update_cost")
            if maliyet_form.is_valid():
                p_cost = maliyet_form.data['product_cost']
                w_cost = maliyet_form.data['warehouse_cost']
                o_id = maliyet_form.data['order_id']
                    
            try :
                update_cost(Fransa,o_id, p_cost, w_cost)
                update_profit(Fransa,o_id , 'EUR')
                return HttpResponseRedirect('../fransa')

            except :
                message = "Maliyet 0 Olamaz"
                data = {
                "info" : d,
                'form' : form,
                'message' : message
                }


        elif 'update_order_list' in request.POST:
            if len(b) == 0 : 
                mailparse(country=Fransa,user = request.user , email=pazarlar.FRMAIL , apppassword=pazarlar.FRPASSWORD , fdate=request.POST['date'])
            else:
                mailparse(country=Fransa,user = request.user , email=pazarlar.FRMAIL , apppassword=pazarlar.FRPASSWORD , fdate=None)
            
            return HttpResponseRedirect('../fransa')
    else:
        print("no form posted")
        form = UploadFileForm()

    
    return render(request , 'fransa.html' , data) 



def update_cost(country,order_id,product_cost,warehouse_cost):
    print('a' + order_id + 'a')
    order = country.objects.get(SATICI_SIPARIS_NUMARASI = order_id)
    print(order)
    order.MALIYET = product_cost
    order.DEPO_MALIYET = warehouse_cost
    order.save()     

 


def update_profit(country,order_id , currency_type):
    order = country.objects.get(SATICI_SIPARIS_NUMARASI = order_id)
    currency = eur_to_usd if currency_type == 'EUR' else gbp_to_usd
    profit = (order.SATIS_FIYATI - order.AMAZON_FEE - order.DEPO_MALIYET) * currency - order.MALIYET
    print('currr', currency)
    print('profit', profit)
    order.KAR = round(profit,2)
    order.YUZDELIK_KAR = round(order.KAR / (order.MALIYET + order.DEPO_MALIYET*currency),3)
    order.save()



def pl(request):
    return render(request , 'pl.html') 