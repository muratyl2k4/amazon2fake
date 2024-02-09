from django.shortcuts import render , redirect
from .models import *
from .fileupload import keepa_excel
from .forms import UploadFileForm
from datetime import datetime
from django.core.files import File
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django_pandas.io import read_frame
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


#download-function
def dbdownload(country , queryset):
    now = datetime.now().strftime("%d_%m_%Y %H_%M_%S")
    df = read_frame(queryset, fieldnames=['Title', 'Asin', 'SalesRank' ,'SalesRank90','Drop_Count' ,
                                          'Buy_Price' , 'Sale_Price' , 'Buybox_Lowest',  'Ratio', 'Cost',
                                          'Profit' , 'Profit_Percentage' , 'Sales_Info' , 'Weight',
                                          'Fba_Seller_Count' , 'Is_Buybox_Fba' , 'Variation_Asins' , 'Amazon_Current'])

    df.rename(columns = {'Title':'Ürün Adı' , 'Asin':'ASIN' , 'SalesRank90' : '90 Gun Sales Rank',  'Drop_Count':'Drop Count' ,
                         'Buy_Price' : 'Alış Fiyatı' , 'Sale_Price' : 'Satış Fiyatı' , 'Buybox_Lowest' : 'Buybox : Lowest' ,
                        'Ratio' : 'Oran', 'Cost' : 'Maliyet',
                        'Profit' : 'Kâr', 'Profit_Percentage' : 'Kâr Yüzde' ,
                          'Sales_Info' : 'Satış Sayısı' ,'Fba_Seller_Count' : 'Fba Satıcı Sayısı' ,'Variation_Asins' : 'Varyasyon Sayisi' ,  'Weight' : 'Ağırlık' ,
                            'Is_Buybox_Fba' : 'Buybox FBA ?' , 'Amazon_Current' : 'Amazon Satıcı ?'}, inplace = True)

    filename= f"{country}_{now}.xlsx"
    df.to_excel(f'amazon2/remote/static/downloaded_datas/{filename}')

    db_path = f'amazon2/remote/static/downloaded_datas/{filename}'
    dbfile = File(open(db_path, "rb"))
    response = HttpResponse(dbfile)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Content-Length'] = dbfile.size

    return response

#filtering func
def product_filter(key , value , data , notOrderedData):
    if value != '':
        if key == 'drop_count_min':
            data['asins'] = data['asins'].filter(Drop_Count__gte = value)
        elif key == 'drop_count_max':
            data['asins'] = data['asins'].filter(Drop_Count__lte = value)

        elif key == 'profit_percentage_min':
            data['asins'] = data['asins'].filter(Profit_Percentage__gte = int(value)/100)
        elif key == 'profit_percentage_max':
            data['asins'] = data['asins'].filter(Profit_Percentage__lte = int(value)/100)

        elif key == 'sales_info_min':
            data['asins'] = data['asins'].filter(Sales_Info__gte = value)
        elif key == 'sales_info_max':
            data['asins'] = data['asins'].filter(Sales_Info__lte = value)

        elif key == 'fba_seller_count_min':
            data['asins'] = data['asins'].filter(Fba_Seller_Count__gte = value)
        elif key == 'fba_seller_count_max':
            data['asins'] = data['asins'].filter(Fba_Seller_Count__lte = value)

        elif key == 'amazon_sale_price_min':
            data['asins'] = data['asins'].filter(Amazon_Current__gte = value)
        elif key == 'amazon_sale_price_max':
            data['asins'] = data['asins'].filter(Amazon_Current__lte = value)

        elif key == 'weight_min':
            data['asins'] = data['asins'].filter(Weight__gte = value)
        elif key == 'weight_max':
            data['asins'] = data['asins'].filter(Weight__lte = value)

        elif key == 'sortByProfitPercentage':
            if value == 'h2l':
                data['asins'] = data['asins'].order_by('Profit_Percentage')
                data['sortByProfitPercentageValue'] = 'l2h'

            elif value == 'l2h':
                data['asins'] = data['asins'].order_by('-Profit_Percentage')
                data['sortByProfitPercentageValue'] = None

            elif value == None:
                data['asins'] = notOrderedData
                data['sortByProfitPercentageValue'] = 'h2l'

        elif key == 'sortByFBASeller':
            if value == 'h2l':
                data['asins'] = data['asins'].order_by('Fba_Seller_Count')
                data['sortByFBASellerValue'] = 'l2h'

            elif value == 'l2h':
                data['asins'] = data['asins'].order_by('-Fba_Seller_Count')
                data['sortByFBASellerValue'] = None

            elif value == None:
                data['asins'] = notOrderedData
                data['sortByFBASellerValue'] = 'h2l'

        elif key == 'sortBySalesInfo':
            if value == 'h2l':
                data['asins'] = data['asins'].order_by('Sales_Info')
                data['sortBySalesInfoValue'] = 'l2h'

            elif value == 'l2h':
                data['asins'] = data['asins'].order_by('-Sales_Info')
                data['sortBySalesInfoValue'] = None

            elif value == None:
                data['asins'] = notOrderedData
                data['sortBySalesInfoValue'] = 'h2l'


@login_required(login_url='login')
def fbaHomePage(request):
    countries = ['uk','ca','ja','au','fr','de']
    data = {
        'countries' : countries
    }
    return render(request,'fbahome.html' , data)
@login_required(login_url='login')
def fbaMarketPage(request,country):
    '''
    out_of_pool_products = None
    completedDatas = None
    notCompletedDatas = None
    keepaExcelDatas = None
    '''

    global switchCase
    switchCase = {
        'fr' : [CompletedFR , NotCompletedFR , KeepaExcelFR],
        'uk' : [CompletedUK , NotCompletedUK , KeepaExcelUK],
        'ca' : [CompletedCA , NotCompletedCA , KeepaExcelCA],
        'ja' : [CompletedJA , NotCompletedJA , KeepaExcelJA],
        'au' : [CompletedAU , NotCompletedAU , KeepaExcelAU],
        'de' : [CompletedDE , NotCompletedDE , KeepaExcelDE],
    }
    completedDatas = switchCase[country][0]
    notCompletedDatas = switchCase[country][1]
    keepaExcelDatas = switchCase[country][2]
    total_asin_in_queue = [i[0] for i in completedDatas.objects.values_list('Asin' , 'Ratio').filter(User= request.user) if i[1] == None]

    queue = {
        'asin_in_queue' : len(total_asin_in_queue),

    }

    out_of_pool_products = completedDatas.objects.filter(~Q(Pool=True) , User = request.user)
    out_of_pool_products = out_of_pool_products.filter(~Q(Is_Deleted_By_User = True))
    form = UploadFileForm(request.POST, request.FILES)
    if not request.user.is_superuser :
        out_of_pool_products = out_of_pool_products.filter(Profit__gte = 0.20)


    global target_link_dict
    target_link_dict = {
        'uk' : 'https://www.amazon.co.uk/dp/',
        'fr' : 'https://www.amazon.fr/dp/',
        'au' : 'https://www.amazon.com.au/dp/',
        'ja' : 'https://www.amazon.co.jp/dp/',
        'de' : 'https://amazon.de/dp/',
        'ca' : 'https://www.amazon.ca/dp/',
    }

    data = {'form' : form ,
            'asins' : out_of_pool_products ,
            'country':[country.upper()],
            'queue' :  queue,
            'sortByProfitPercentageValue' : 'h2l' ,
            'sortByFBASellerValue' : 'h2l' ,
            'sortBySalesInfoValue' : 'h2l' ,
            'target_link' : target_link_dict[country]
            }

    if request.method == 'GET':

        for key,value in request.GET.items():
            product_filter(key=key , value=value , data=data , notOrderedData=out_of_pool_products)

    if request.method == 'POST':

        if 'asin_text_upload' in request.POST:
            asins = request.POST['asintext'].split('\n')
            for asin in asins:
                if not asin == '':
                    asin = asin.strip(' ').strip('\r')

                    try:
                        check = completedDatas.objects.filter(~Q(Profit_Percentage = None) , Asin= asin)
                        check2nd = datetime.now().date() - check[0].Date
                        if (check2nd).days >=1:
                            try :
                                product = notCompletedDatas.objects.get(Asin = asin)

                            except:
                                notcompleted = notCompletedDatas(Asin = asin)
                                notcompleted.save()
                            finally :
                                product = completedDatas(User= request.user , Asin=asin)
                                product.save()
                        else :
                            try :
                                existing_user_product = check.filter(User= request.user)
                                existing_user_product = existing_user_product[0]
                                if existing_user_product.Is_Deleted_By_User == True:
                                    existing_user_product.Is_Deleted_By_User = False
                                    existing_user_product.save()
                            except:
                                #test edilecek
                                new = check[0]
                                new._state.adding = True
                                new.pk = None
                                new.User = request.user
                                new.Is_Deleted_By_User = False
                                new.save(using='mysql')
                    except:
                        try:
                            product_keepa = keepaExcelDatas.objects.get(Asin = asin)
                            product = completedDatas(User= request.user ,
                                                    Title = product_keepa.Title ,
                                                    Asin=asin ,
                                                    SalesRank = product_keepa.SalesRank,
                                                    SalesRank90 = product_keepa.SalesRank90,
                                                    Is_Buybox_Fba = product_keepa.Is_Buybox_Fba ,
                                                    Buybox_Lowest = product_keepa.Buybox_Lowest ,
                                                    Variation_Asins = product_keepa.Variation_Asins ,
                                                    Fba_Seller_Count = product_keepa.Fba_Seller_Count ,
                                                    Weight = product_keepa.Weight ,
                                                    Amazon_Current = product_keepa.Amazon_Current)
                            product.save()
                        except:
                            try :
                                product = notCompletedDatas.objects.get(Asin = asin)

                            except:
                                notcompleted = notCompletedDatas(Asin = asin)
                                notcompleted.save()
                            finally:
                                product = completedDatas(User= request.user , Asin=asin)
                                product.save()

        elif 'asin_file_upload' in request.POST:
            excelData(com_asin=request.FILES.get('com_asin') ,
                        target_asin=request.FILES.get('target_asin') ,
                        Userx = request.user,
                        Market= country).save()

            messages.success(request , "Ürünleriniz taranmaya başlanmıştır!")
            return redirect(f"../fba/{country}")

            """
            excelData(com_asin=request.FILES.get('com_asin') ,
                        target_asin=request.FILES.get('target_asin') ,
                        Userx = request.user,
                        Market = country).save()
            elif 'asin_link_upload' in request.POST:
                product = StoreLink(User = request.user ,
                                    Link = request.POST['storelink'],
                                    Marketplace = country)
                product.save()
            """
        elif 'send_pool' in request.POST:
            asin_list = request.POST.getlist('poolCheckBox')
            for asin in asin_list:
                product_to_pool =completedDatas.objects.get(User = request.user , Asin=asin)
                product_to_pool.Pool = True
                product_to_pool.save()
        elif 'download_products' in request.POST:
            asin_list = request.POST.getlist('poolCheckBox')
            return dbdownload(country=country , queryset= out_of_pool_products.filter(Asin__in = asin_list))

        elif 'delete_products' in request.POST:
            asin_list = request.POST.getlist('poolCheckBox')
            for asin in asin_list:
                try :
                    product_to_delete = completedDatas.objects.get(User = request.user , Asin = asin)
                    product_to_delete.Is_Deleted_By_User = True
                    product_to_delete.save()
                except :
                    products_to_delete =completedDatas.objects.filter(User = request.user , Asin=asin)
                    for product_to_delete in products_to_delete:
                        product_to_delete.Is_Deleted_By_User = True
                        product_to_delete.save()
        elif 'all_selected' in request.POST:
            if request.POST['selected_all_choices'] == 'send_pool_all':
                out_of_pool_products.update(Pool = True)

            elif request.POST['selected_all_choices'] == 'download_all':
                 return dbdownload(country=country , queryset= out_of_pool_products)
            elif request.POST['selected_all_choices'] == 'delete_all':
                out_of_pool_products.update(Is_Deleted_By_User = True)


    paginator = Paginator(data['asins'] , 100)
    page_number = request.GET.get("page")
    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    len_all_products = len(data['asins'])

    data['len_all_products'] = len_all_products

    data['asins'] = page_obj
    return render(request,'fbamarket.html' , data)



@login_required(login_url='login')
def fbaMarketPoolPage(request,country):



    Completed_Model = switchCase[country][0]
    poolDatas = Completed_Model.objects.filter(User = request.user , Pool = True)
    poolDatas = poolDatas.filter(~Q(Is_Deleted_By_User = True))


    data = {
        'asins' : poolDatas ,
        'country' : [country.upper()],
        'sortByProfitPercentageValue' : 'h2l' ,
        'sortByFBASellerValue' : 'h2l' ,
        'sortBySalesInfoValue' : 'h2l' ,
        'target_link' : target_link_dict[country]
    }
    if request.method == 'GET':

        for key,value in request.GET.items():
            product_filter(key=key , value=value , data=data , notOrderedData=poolDatas)
    if request.method == 'POST':
        if 'send_pool' in request.POST:
            asin_list = request.POST.getlist('poolCheckBox')

            for asin in asin_list:
                product_to_pool =Completed_Model.objects.get(User = request.user , Asin=asin)
                product_to_pool.Pool = False
                product_to_pool.save()
        elif 'download_products' in request.POST:
            asin_list = request.POST.getlist('poolCheckBox')
            return dbdownload(country=country , queryset=poolDatas.filter(Asin__in = asin_list) if not len(asin_list) == 0 else poolDatas)


    paginator = Paginator(data['asins'] , 100)
    page_number = request.GET.get("page")
    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    data['asins'] = page_obj

    return render(request,'fbamarketpool.html' , data)

def fbaMarketDeletedPage(request , country):
    Completed_Model = switchCase[country][0]
    Deleted_Asins = Completed_Model.objects.filter(User = request.user , Is_Deleted_By_User = True)
    data = {
        'asins' : Deleted_Asins,
        'country' : [country.upper()],
        'sortByProfitPercentageValue' : 'h2l' ,
        'sortByFBASellerValue' : 'h2l' ,
        'sortBySalesInfoValue' : 'h2l' ,
        'target_link' : target_link_dict[country]
    }

    if request.method == 'GET':

        for key,value in request.GET.items():
            product_filter(key=key , value=value , data=data , notOrderedData=Deleted_Asins)

    if request.method == 'POST':
        if 'get_asins_back' in request.POST:
            asin_list = request.POST.getlist('deletedAsinsCheckBox')
            for asin in asin_list:
                try :
                    products_to_reupload =Deleted_Asins.get(User = request.user , Asin=asin)
                    product_to_reupload.Is_Deleted_By_User = False
                    product_to_reupload.save()
                except :
                    products_to_reupload =Deleted_Asins.filter(User = request.user , Asin=asin)
                    for product_to_reupload in products_to_reupload:
                        product_to_reupload.Is_Deleted_By_User = False
                        product_to_reupload.save()

    paginator = Paginator(data['asins'] , 100)
    page_number = request.GET.get("page")
    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    data['asins'] = page_obj
    return render(request , 'fbamarketdeleted.html' , data)