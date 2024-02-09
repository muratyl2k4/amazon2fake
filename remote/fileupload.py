import pandas as pd
from .models import *
from datetime import datetime
from django.db.models import Q


'''
##TODO
class Keepa_Excel():
    def __init__(self , completed_db , keepa_db ,notCompleted_db , user):
        self.completed_db = completed_db
        self.keepa_db = keepa_db
        self.notCompleted_db = notCompleted_db
        self.user = user
'''


##main function
def keepa_excel(com_file , target_file , keepa_db , completed_db , notCompleted_db , user):
    try :
        ##select columns from xlsx
        com_pd_file =pd.read_excel(com_file)[['Title','ASIN','Buy Box: Current','New: Current','New, 3rd Party FBA: Current','New, 3rd Party FBM: Current']]
        target_pd_file = pd.read_excel(target_file)[['ASIN','Sales Rank: Current','Sales Rank: Drops last 30 days','Buy Box: Current','New: Current','New, 3rd Party FBA: Current','New, 3rd Party FBM: Current','Referral Fee %','FBA Fees:','Buy Box: Is FBA','Count of retrieved live offers: New, FBA' , 'Amazon: Current' , 'Package: Dimension (cm³)' ,  'Package: Weight (g)' , 'Sales Rank: 90 days avg.' , 'Buy Box: Lowest' , 'Variation ASINs']]
        ##rename columns for db
        columns_to_rename_com = {'New, 3rd Party FBM: Current':'Buy_Price_FBM',
        'New, 3rd Party FBA: Current':'Buy_Price_FBA',
        'New: Current':'Buy_Price_NC',
        'Buy Box: Current':'Buy_Price_BB'}


        columns_to_rename_target = {'Sales Rank: Current':'SalesRank',
        'Sales Rank: Drops last 30 days':'Drop_Count',
        'New, 3rd Party FBM: Current':'Sale_Price_FBM',
        'New, 3rd Party FBA: Current':'Sale_Price_FBA',
        'New: Current':'Sale_Price_NC',
        'Buy Box: Current':'Sale_Price_BB',
        'Referral Fee %':'Referral_Fee_Percentage',
        'FBA Fees:':'Pick_and_Pack_Fee',
        'Buy Box: Is FBA':'Is_Buybox_Fba',
        'Count of retrieved live offers: New, FBA':'Fba_Seller_Count',
        'Amazon: Current':'Amazon_Current',
        'Package: Dimension (cm³)':'Dimension',
        'Package: Weight (g)':'Weight',
        'Sales Rank: 90 days avg.' : 'SalesRank90' ,
        'Buy Box: Lowest' : 'Buybox_Lowest' ,
        'Variation ASINs' : 'Variation_Asins'}


        # Rename DataFrame Columns
        com_pd_file.rename(columns = columns_to_rename_com , inplace = True)
        target_pd_file.rename(columns = columns_to_rename_target , inplace=True)
        print('---')
        print(type(com_pd_file))
        print(type(target_pd_file))
        print('---')
        print(com_pd_file)

        print('1')
        ## Merge And Drop Na's
        df_to_work = pd.merge(com_pd_file, target_pd_file, on=["ASIN" , 'ASIN'])
        print('2')
        df_to_work = df_to_work.fillna(-21)
        print('3')


        ##convert dataframes columns to a python list(fastest way i found -murat)
        ASINlist = df_to_work['ASIN'].values
        TITLElist = df_to_work['Title'].values
        SALESRANKlist = df_to_work['SalesRank'].values
        FBA_SELLER_COUNTlist = df_to_work['Fba_Seller_Count'].values
        AMAZON_CURRENTlist = df_to_work['Amazon_Current'].values
        WEIGHTlist = df_to_work['Weight'].values
        DIMENSIONlist = df_to_work['Dimension'].values
        DROP_COUNTlist = df_to_work['Drop_Count'].values
        IS_BUYBOX_FBAlist = df_to_work['Is_Buybox_Fba'].values
        BUY_PRICE_FBAlist = df_to_work['Buy_Price_FBA'].values
        BUY_PRICE_FBMlist = df_to_work['Buy_Price_FBM'].values
        BUY_PRICE_BBlist = df_to_work['Buy_Price_BB'].values
        BUY_PRICE_NClist = df_to_work['Buy_Price_NC'].values
        SALE_PRICE_FBAlist = df_to_work['Sale_Price_FBA'].values
        SALE_PRICE_FBMlist = df_to_work['Sale_Price_FBM'].values
        SALE_PRICE_BBlist = df_to_work['Sale_Price_BB'].values
        SALE_PRICE_NClist = df_to_work['Sale_Price_NC'].values
        REFERRAL_FEE_PERCENTAGElist = df_to_work['Referral_Fee_Percentage'].values
        PICK_AND_PACK_FEElist = df_to_work['Pick_and_Pack_Fee'].values
        SALESRANK90list = df_to_work['SalesRank90'].values
        BUYBOX_LOWESTlist = df_to_work['Buybox_Lowest'].values
        VARIATION_ASINSlist = df_to_work['Variation_Asins'].values
        ##global degerler tum fonksiyonlara tek tek gondermemek icin
        global ASIN , TITLE , SALESRANK , Is_Buybox_Fba_check , FBA_SELLER_COUNT , AMAZON_CURRENT , WEIGHT , DIMENSION  ,DROP_COUNT
        global BUY_PRICE_FBA,BUY_PRICE_FBM,BUY_PRICE_BB,BUY_PRICE_NC
        global SALE_PRICE_FBA,SALE_PRICE_FBM,SALE_PRICE_BB,SALE_PRICE_NC
        global REFERRAL_FEE_PERCENTAGE , PICK_AND_PACK_FEE , VARIATION_ASINS , BUYBOX_LOWEST , SALESRANK90

        for asin in range(len(df_to_work)):
            ##changing is buybox fba value(yes,no) to True or False
            Is_Buybox_Fba_check = IS_BUYBOX_FBAlist[asin]
            if Is_Buybox_Fba_check==  'yes': Is_Buybox_Fba_check = True
            elif Is_Buybox_Fba_check==  'no': Is_Buybox_Fba_check = False

            ##values completedDb
            ASIN = ASINlist[asin]
            TITLE = TITLElist[asin]
            SALESRANK = SALESRANKlist[asin]
            FBA_SELLER_COUNT = FBA_SELLER_COUNTlist[asin]
            AMAZON_CURRENT = AMAZON_CURRENTlist[asin]
            WEIGHT = WEIGHTlist[asin]
            DIMENSION = DIMENSIONlist[asin]
            SALESRANK90 = SALESRANK90list[asin]
            BUYBOX_LOWEST = BUYBOX_LOWESTlist[asin]
            VARIATION_ASINS = VARIATION_ASINSlist[asin]
            ##values for keepaDb
            DROP_COUNT = DROP_COUNTlist[asin]
            BUY_PRICE_FBA = BUY_PRICE_FBAlist[asin]
            BUY_PRICE_FBM = BUY_PRICE_FBMlist[asin]
            BUY_PRICE_BB = BUY_PRICE_BBlist[asin]
            BUY_PRICE_NC = BUY_PRICE_NClist[asin]
            SALE_PRICE_FBA = SALE_PRICE_FBAlist[asin]
            SALE_PRICE_FBM = SALE_PRICE_FBMlist[asin]
            SALE_PRICE_BB = SALE_PRICE_BBlist[asin]
            SALE_PRICE_NC = SALE_PRICE_NClist[asin]
            REFERRAL_FEE_PERCENTAGE = REFERRAL_FEE_PERCENTAGElist[asin]
            PICK_AND_PACK_FEE = PICK_AND_PACK_FEElist[asin]
            try:
                check = completed_db.objects.filter(~Q(Profit_Percentage = None) , Asin= ASIN)
                check2nd = datetime.now().date() - check[0].Date
                if (check2nd).days >=1:
                    check_to_notCompleted_db(notCompleted_db=notCompleted_db ,
                                         completed_db=completed_db ,
                                         keepa_db=keepa_db ,
                                         user=user,
                                         )

                    existing_user_product = check.filter(User= user)
                    existing_user_product = existing_user_product[0]
                    if existing_user_product.Is_Deleted_By_User == True:
                        existing_user_product.Is_Deleted_By_User = False
                        existing_user_product.save()
                else :
                    try :
                        existing_user_product = check.filter(User= user)
                        existing_user_product = existing_user_product[0]
                        if existing_user_product.Is_Deleted_By_User == True:
                            existing_user_product.Is_Deleted_By_User = False
                            existing_user_product.save()
                            check_to_notCompleted_db(notCompleted_db=notCompleted_db ,
                                         completed_db=completed_db ,
                                         keepa_db=keepa_db ,
                                         user=user,)
                    except:

                        existing_product = check[0]
                        existing_product._state.adding = True
                        existing_product.pk = None
                        existing_product.User = user
                        existing_product.Is_Deleted_By_User = False
                        existing_product.Pool = False
                        existing_product.save(using='mysql')
            except Exception as e:
                check_to_notCompleted_db(notCompleted_db=notCompleted_db ,
                                         completed_db=completed_db ,
                                         keepa_db=keepa_db ,
                                         user=user,)

    except Exception as e:
        print('Excel Hatali')
        print(e)


##check not completed ,fill other users fields and delete asin in notcompleted_db
def check_to_notCompleted_db(notCompleted_db , completed_db , keepa_db ,user ):
    global ASIN , TITLE , SALESRANK , Is_Buybox_Fba_check , FBA_SELLER_COUNT , AMAZON_CURRENT , WEIGHT , DIMENSION  ,DROP_COUNT
    global BUY_PRICE_FBA,BUY_PRICE_FBM,BUY_PRICE_BB,BUY_PRICE_NC
    global SALE_PRICE_FBA,SALE_PRICE_FBM,SALE_PRICE_BB,SALE_PRICE_NC
    global REFERRAL_FEE_PERCENTAGE , PICK_AND_PACK_FEE , VARIATION_ASINS , BUYBOX_LOWEST , SALESRANK90

    try:
        data = notCompleted_db.objects.get(Asin = ASIN)
        data.delete()

        data = completed_db.objects.filter(Title = None , Asin = ASIN)
        for a in data:
            a.Title = TITLE
            a.SalesRank = SALESRANK
            a.SalesRank90 = SALESRANK90
            a.Is_Buybox_Fba = Is_Buybox_Fba_check if not Is_Buybox_Fba_check == -21 else None
            a.Fba_Seller_Count = FBA_SELLER_COUNT
            a.Amazon_Current = AMAZON_CURRENT
            a.Buybox_Lowest = BUYBOX_LOWEST
            if not VARIATION_ASINS == -21:
                a.Variation_Asins = VARIATION_ASINS.count(',') +1
            else :
                a.Variation_Asins = -21

            a.Weight = max(WEIGHT * 0.0022046226 , DIMENSION * 0.0610237 /135)
            a.save()
    except Exception as e:
        None
    finally:
        dataSaver(completed_db=completed_db ,
                keepa_db=keepa_db ,
                user=user , )



#main keepa_db saving method
def dataSaver(completed_db , keepa_db , user):
    global ASIN , TITLE , SALESRANK , Is_Buybox_Fba_check , FBA_SELLER_COUNT , AMAZON_CURRENT , WEIGHT , DIMENSION  ,DROP_COUNT
    global BUY_PRICE_FBA,BUY_PRICE_FBM,BUY_PRICE_BB,BUY_PRICE_NC
    global SALE_PRICE_FBA,SALE_PRICE_FBM,SALE_PRICE_BB,SALE_PRICE_NC
    global REFERRAL_FEE_PERCENTAGE , PICK_AND_PACK_FEE , VARIATION_ASINS , BUYBOX_LOWEST , SALESRANK90

    try:
        data = keepa_db.objects.get(Asin = ASIN)

    except Exception as e:
        data = keepa_db(Asin = ASIN ,
            Title = TITLE,
            SalesRank = SALESRANK,
            SalesRank90 = SALESRANK90 ,
            Drop_Count = DROP_COUNT,
            Buy_Price_FBA = BUY_PRICE_FBA,
            Buy_Price_FBM = BUY_PRICE_FBM,
            Buy_Price_BB = BUY_PRICE_BB,
            Buy_Price_NC = BUY_PRICE_NC,
            Sale_Price_NC = SALE_PRICE_NC,
            Sale_Price_BB = SALE_PRICE_BB,
            Sale_Price_FBM = SALE_PRICE_FBM,
            Sale_Price_FBA = SALE_PRICE_FBA,
            Buybox_Lowest =BUYBOX_LOWEST,
            Is_Buybox_Fba = Is_Buybox_Fba_check if not Is_Buybox_Fba_check == -21 else None ,
            Amazon_Current = AMAZON_CURRENT ,
            Fba_Seller_Count = FBA_SELLER_COUNT ,
            Variation_Asins = VARIATION_ASINS.count(',') if not VARIATION_ASINS == -21 else None ,
            Weight = max(WEIGHT * 0.0022046226 , DIMENSION * 0.0610237 /135),
            Referral_Fee_Percentage = REFERRAL_FEE_PERCENTAGE,
            Pick_and_Pack_Fee = PICK_AND_PACK_FEE
            )
        data.save(using='mysql')
    finally:
        get_or_create_completed(completed_db=completed_db ,
                            user=user )



## check the completed have that asin for user
def get_or_create_completed(completed_db , user):
    global ASIN , TITLE , SALESRANK , Is_Buybox_Fba_check , FBA_SELLER_COUNT , AMAZON_CURRENT , WEIGHT , DIMENSION  ,DROP_COUNT
    global BUY_PRICE_FBA,BUY_PRICE_FBM,BUY_PRICE_BB,BUY_PRICE_NC
    global SALE_PRICE_FBA,SALE_PRICE_FBM,SALE_PRICE_BB,SALE_PRICE_NC
    global REFERRAL_FEE_PERCENTAGE , PICK_AND_PACK_FEE , VARIATION_ASINS , BUYBOX_LOWEST , SALESRANK90



    try:
        check = completed_db.objects.get(User = user ,
                                        Asin = ASIN ,
                                        )
    except Exception as e:
        #1
        new = completed_db(
                        User = user ,
                        Title = TITLE,
                        Asin = ASIN ,
                        SalesRank = SALESRANK ,
                        SalesRank90 = SALESRANK90,
                        Is_Buybox_Fba = Is_Buybox_Fba_check if not Is_Buybox_Fba_check == -21 else None ,
                        Fba_Seller_Count = FBA_SELLER_COUNT ,
                        Amazon_Current = AMAZON_CURRENT ,
                        Buybox_Lowest = BUYBOX_LOWEST ,
                        Variation_Asins = VARIATION_ASINS.count(',') if not VARIATION_ASINS == -21 else None ,
                        Weight = max(WEIGHT * 0.0022046226 , DIMENSION * 0.0610237 /135)
                        )
        new.save(using='mysql')


