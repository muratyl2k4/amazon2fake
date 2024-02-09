from datetime import datetime
import pandas as pd

def get_excels(com_file , target_file , cursor ,keepa_db_query , completed_db_query , notCompleted_db_query , user_id):

    try:
        com_pd_file =pd.read_excel(com_file)[['Title','ASIN','Buy Box: Current','New: Current','New, 3rd Party FBA: Current','New, 3rd Party FBM: Current']]
        target_pd_file = pd.read_excel(target_file)[['ASIN','Sales Rank: Current','Sales Rank: Drops last 30 days','Buy Box: Current','New: Current','New, 3rd Party FBA: Current','New, 3rd Party FBM: Current','Referral Fee %','FBA Fees:','Buy Box: Is FBA','Count of retrieved live offers: New, FBA' , 'Amazon: Current' , 'Package: Dimension (cm³)' ,  'Package: Weight (g)' , 'Sales Rank: 90 days avg.' , 'Buy Box: Lowest' , 'Variation ASINs']]

        keepa_db = pd.read_sql(keepa_db_query , cursor).fillna(-33)
        completed_db = pd.read_sql(completed_db_query ,cursor ).fillna(-33)
        notCompleted_db = pd.read_sql(notCompleted_db_query ,cursor ).fillna(-33)

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

        ## Merge And Drop Na's
        df_to_work = pd.merge(com_pd_file, target_pd_file, on=["ASIN" , 'ASIN'])
        df_to_work = df_to_work.fillna(-21)

        change_IDBU_true_df = pd.DataFrame(columns=completed_db.columns)

        existing_products_df = pd.DataFrame(columns=completed_db.columns)

        Asins_to_delete_from_notCompleted = []

        fill_empty_rows_df = pd.DataFrame(columns=completed_db.columns)

        add_to_keepa_db_df = pd.DataFrame(columns= keepa_db.columns)

        new_completed_db_df = pd.DataFrame(columns=completed_db.columns)

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

            check = completed_db[(completed_db.Profit_Percentage != -33) & (completed_db.Asin == ASIN)]
            if len(check.index) >= 1:
                existing_user_product = check[(check.User_id == user_id) & (check.Is_Deleted_By_User == True)]
                if len(existing_user_product.index) >= 1:
                    existing_user_product = existing_user_product.iloc[0]

                    change_IDBU_true_df.loc[len(change_IDBU_true_df.index)] = existing_user_product

                time_difference_by_product = datetime.now().date() - check.iloc[0].Date
                if not time_difference_by_product.days >=0:

                    existing_product = check.iloc[0]
                    existing_product.User_id = user_id
                    existing_product.Is_Deleted_By_User = False
                    existing_product.Pool = False

                    existing_products_df.loc[len(existing_products_df.index)] = existing_product

            check_to_notCompleted_db(notCompleted_db=notCompleted_db ,completed_db=completed_db , keepa_db=keepa_db ,
                                    user=user_id,ASIN=ASIN , TITLE=TITLE , SALESRANK=SALESRANK , Is_Buybox_Fba_check=Is_Buybox_Fba_check,
                                    FBA_SELLER_COUNT=FBA_SELLER_COUNT , AMAZON_CURRENT=AMAZON_CURRENT , WEIGHT=WEIGHT , DIMENSION=DIMENSION,
                                    DROP_COUNT=DROP_COUNT,BUY_PRICE_FBA=BUY_PRICE_FBA, BUY_PRICE_FBM=BUY_PRICE_FBM, BUY_PRICE_BB=BUY_PRICE_BB,
                                    BUY_PRICE_NC=BUY_PRICE_NC, SALE_PRICE_FBA=SALE_PRICE_FBA,SALE_PRICE_FBM=SALE_PRICE_FBM, SALE_PRICE_BB=SALE_PRICE_BB,
                                    SALE_PRICE_NC=SALE_PRICE_NC,REFERRAL_FEE_PERCENTAGE=REFERRAL_FEE_PERCENTAGE, PICK_AND_PACK_FEE=PICK_AND_PACK_FEE,
                                    VARIATION_ASINS=VARIATION_ASINS , BUYBOX_LOWEST=BUYBOX_LOWEST, SALESRANK90=SALESRANK90,
                                    Asins_to_delete_from_notCompleted=Asins_to_delete_from_notCompleted , fill_empty_rows_df=fill_empty_rows_df , add_to_keepa_db_df = add_to_keepa_db_df,
                                    new_completed_db_df = new_completed_db_df)

        return [change_IDBU_true_df , existing_products_df , Asins_to_delete_from_notCompleted , fill_empty_rows_df , add_to_keepa_db_df , new_completed_db_df]
    except Exception as e:
        print('Excel Hatali' , e)

##check not completed ,fill other users fields and delete asin from notcompleted_db
def check_to_notCompleted_db(notCompleted_db , completed_db , keepa_db ,user , ASIN , TITLE , SALESRANK , Is_Buybox_Fba_check ,
                            FBA_SELLER_COUNT , AMAZON_CURRENT , WEIGHT , DIMENSION  ,DROP_COUNT
                            ,BUY_PRICE_FBA,BUY_PRICE_FBM,BUY_PRICE_BB,BUY_PRICE_NC
                            ,SALE_PRICE_FBA,SALE_PRICE_FBM,SALE_PRICE_BB,SALE_PRICE_NC
                            ,REFERRAL_FEE_PERCENTAGE , PICK_AND_PACK_FEE , VARIATION_ASINS , BUYBOX_LOWEST , SALESRANK90
                            ,Asins_to_delete_from_notCompleted , fill_empty_rows_df , add_to_keepa_db_df , new_completed_db_df):

    data = notCompleted_db[notCompleted_db.Asin == ASIN]
    if len(data) >= 1:

        Asins_to_delete_from_notCompleted.append(data['Asin'])
        data = completed_db[(completed_db.Title == None) & (completed_db.Asin == ASIN)]
        ## fill empty row's values
        for has_empty_values_row in range(len(data.index)):
            has_empty_values_row = data.iloc[has_empty_values_row]
            has_empty_values_row.Title = TITLE
            has_empty_values_row.SalesRank = SALESRANK
            has_empty_values_row.SalesRank90 = SALESRANK90
            has_empty_values_row.Is_Buybox_Fba = Is_Buybox_Fba_check if not Is_Buybox_Fba_check == -21 else None
            has_empty_values_row.Fba_Seller_Count = FBA_SELLER_COUNT
            has_empty_values_row.Amazon_Current = AMAZON_CURRENT
            has_empty_values_row.Buybox_Lowest = BUYBOX_LOWEST
            if not VARIATION_ASINS == -21:
                has_empty_values_row.Variation_Asins = VARIATION_ASINS.count(',') +1
            else :
                has_empty_values_row.Variation_Asins = -21

            has_empty_values_row.Weight = max(WEIGHT * 0.0022046226 , DIMENSION * 0.0610237 /135)

        fill_empty_rows_df = pd.concat([fill_empty_rows_df, data])


    dataSaver(completed_db=completed_db , keepa_db=keepa_db ,user=user , ASIN=ASIN , TITLE=TITLE , SALESRANK=SALESRANK,
              Is_Buybox_Fba_check=Is_Buybox_Fba_check , FBA_SELLER_COUNT=FBA_SELLER_COUNT , AMAZON_CURRENT=AMAZON_CURRENT,
               WEIGHT=WEIGHT, DIMENSION=DIMENSION, DROP_COUNT=DROP_COUNT , BUY_PRICE_FBA=BUY_PRICE_FBA,BUY_PRICE_FBM=BUY_PRICE_FBM,
                BUY_PRICE_BB=BUY_PRICE_BB,BUY_PRICE_NC=BUY_PRICE_NC,SALE_PRICE_FBA=SALE_PRICE_FBA,SALE_PRICE_FBM=SALE_PRICE_FBM,
                 SALE_PRICE_BB=SALE_PRICE_BB,SALE_PRICE_NC=SALE_PRICE_NC,REFERRAL_FEE_PERCENTAGE=REFERRAL_FEE_PERCENTAGE,
                  PICK_AND_PACK_FEE=PICK_AND_PACK_FEE,VARIATION_ASINS=VARIATION_ASINS, BUYBOX_LOWEST=BUYBOX_LOWEST, SALESRANK90=SALESRANK90,
                    add_to_keepa_db_df=add_to_keepa_db_df , new_completed_db_df=new_completed_db_df)

#main keepa_db saving method
def dataSaver(completed_db , keepa_db , user, ASIN , TITLE , SALESRANK , Is_Buybox_Fba_check , FBA_SELLER_COUNT ,
               AMAZON_CURRENT , WEIGHT , DIMENSION  ,DROP_COUNT  ,BUY_PRICE_FBA,BUY_PRICE_FBM,BUY_PRICE_BB,
               BUY_PRICE_NC ,SALE_PRICE_FBA,SALE_PRICE_FBM,SALE_PRICE_BB,SALE_PRICE_NC,REFERRAL_FEE_PERCENTAGE ,
                PICK_AND_PACK_FEE , VARIATION_ASINS , BUYBOX_LOWEST , SALESRANK90 ,add_to_keepa_db_df , new_completed_db_df):

    if not len(keepa_db[keepa_db.Asin == ASIN].index) >= 1:

        new_keepa_row = dict(Asin = ASIN ,
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
        add_to_keepa_db_df.loc[len(add_to_keepa_db_df.index)] = new_keepa_row
    get_or_create_completed(completed_db=completed_db ,
                        user=user , ASIN=ASIN ,  TITLE=TITLE , SALESRANK=SALESRANK , SALESRANK90=SALESRANK90,
                        Is_Buybox_Fba_check=Is_Buybox_Fba_check , FBA_SELLER_COUNT=FBA_SELLER_COUNT , AMAZON_CURRENT=AMAZON_CURRENT,
                        WEIGHT=WEIGHT , DIMENSION=DIMENSION, VARIATION_ASINS=VARIATION_ASINS, BUYBOX_LOWEST=BUYBOX_LOWEST ,
                          new_completed_db_df=new_completed_db_df)


## check the completed have that asin for user
## TODO eger yukarda existingden gelmis ise burada tekrar sorgu atip duplicate etmesine sebebiyet veriyor
## kesin olarak duzeltilecek !!!!!!!
def get_or_create_completed(completed_db , user , ASIN , TITLE , SALESRANK , Is_Buybox_Fba_check , FBA_SELLER_COUNT ,
                             AMAZON_CURRENT , WEIGHT , DIMENSION ,
                            VARIATION_ASINS , BUYBOX_LOWEST , SALESRANK90,
                            new_completed_db_df):

    if not len(completed_db[(completed_db.User_id == user) & (completed_db.Asin == ASIN)].index) >= 1:
        try:
            #1
            new_completed_db_row = dict(
                            User_id = user ,
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

            new_completed_db_df.loc[len(new_completed_db_df.index)] = new_completed_db_row
        except Exception as e:
            print(e)