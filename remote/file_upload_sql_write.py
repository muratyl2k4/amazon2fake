import datetime
import MySQLdb
import sshtunnel
from sqlalchemy import create_engine

import pandas as pd
sshtunnel.SSH_TIMEOUT = 15.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

def value_creator(val):
    if val == None:
        return 'NULL'
    typ = type(val)
    if typ == str:
        val = f'"{val}"'
    else :
        if not val== -21:
            val = str(val)
        else :
            val = 'NULL'
    return val

def write_to_db(engine, frame, table_name, chunk_size):
    start_index = 0
    end_index = chunk_size if chunk_size < len(frame) else len(frame)

    if_exists_param = 'append'

    while start_index != end_index:
        print("Writing rows %s through %s" % (start_index, end_index))
        frame.iloc[start_index:end_index, :].to_sql(con=engine, name=table_name, if_exists=if_exists_param , index=False)

        start_index = min(start_index + chunk_size, len(frame))
        end_index = min(end_index + chunk_size, len(frame))

import file_upload_task

connection = MySQLdb.connect(
    user='jaylee54',
    password='muratyl1A',
    host='jaylee54.mysql.pythonanywhere-services.com', port=3306,
    database='jaylee54$deneme2',
)
cursor = connection.cursor()

countries = ['uk' , 'ca' , 'de' , 'fr' , 'au' , 'ja']
query= '''SELECT * FROM remote_exceldata WHERE Is_executed = 0'''


uploaded_files_db = pd.read_sql(query , connection)
for excel_file in range(len(uploaded_files_db.index)):
    country = uploaded_files_db.iloc[excel_file].Market
    query_keepa = f'''SELECT * FROM remote_keepaexcel{country}'''
    query_completed = f'''SELECT * FROM remote_completed{country}'''
    query_notcompleted = f'''SELECT * FROM remote_notcompleted{country}'''

    #Index 0: Is_Deleted_By_User False yapilacaklar pd.DataFrame
    #Index 1: Zaten gun icinde taranmis baskasında olan urun pd.DataFrame
    #Index 2: not completed table'indan silinecek olan asinler list[]
    #Index 3: Text olarak yuklenmis asinleri sildikten sonra yukleyenlerin bos verilerini dosyadan tamamlama pd.DataFrame
    #Index 4: Keepa DB'ye eklenecekler  pd.DataFrame
    #Index 5: Completed DB'ye eklenecekler
    result_list = file_upload_task.get_excels(com_file=uploaded_files_db.iloc[excel_file].com_asin , target_file=uploaded_files_db.iloc[excel_file].target_asin , cursor=connection,
                keepa_db_query=query_keepa,
                completed_db_query=query_completed,
                notCompleted_db_query=query_notcompleted , user_id=uploaded_files_db.iloc[excel_file].Userx_id)
    try:
        #1
        change_idbu_df = result_list[0]
        for asin in range(len(change_idbu_df.index)):
            query = f'''UPDATE remote_completed{country} SET Is_Deleted_By_User = 0 WHERE id={change_idbu_df.iloc[asin].id}'''
            cursor.execute(query)
        #2
        existing_products_df = result_list[1].drop(columns=['id'])

        #3
        asins_to_delete_from_nc_db = result_list[2]
        query_str = '"' + '","'.join(map(str , asins_to_delete_from_nc_db)) + '"'

        query = f'DELETE FROM remote_completed{country} WHERE Asin IN ({query_str})'
        cursor.execute(query)
        #4
        fill_empty_rows_df = result_list[3].drop(columns=['id'])
        cols = fill_empty_rows_df.columns
        for asin in range(len(fill_empty_rows_df.index)):
            query_str = ''
            for i in range(len(cols)):
                query_str = f'{cols[i]} = {value_creator(fill_empty_rows_df.iloc[asin].values[i])} ,'
                query = f'UPDATE remote_completed{country} SET {query_str} WHERE Asin = "{fill_empty_rows_df.iloc[asin].Asin}"'
                cursor.execute(query)
        #5
        add_to_keepa_db_df = result_list[4].drop(columns=['id'])
        query_str3 = ','.join(map(str , add_to_keepa_db_df.columns))
        for asin in range(len(add_to_keepa_db_df.index)):
            add_to_keepa_db_df.at[asin, 'Title'] = add_to_keepa_db_df.iloc[asin].Title.replace("\\" , '').replace('"' , '')
            values = ','.join(map(value_creator , add_to_keepa_db_df.iloc[asin].values))
            try:
                query = f'''INSERT INTO remote_keepaexcel{country} ({query_str3}) VALUES ({values})'''
                cursor.execute(query)
            except:
                try:

                    add_to_keepa_db_df.at[asin,'Title'] = '---'
                    values = ','.join(map(value_creator , add_to_keepa_db_df.iloc[asin].values))
                    query = f'''INSERT INTO remote_keepaexcel{country} ({query_str3}) VALUES ({values})'''
                    cursor.execute(query)
                except Exception as e:
                    print(e , values)


        #6
        add_to_completed_db_df = result_list[5].drop(columns=['id'])


        #merge 2 and 6 and drop duplicates
        merged_df = pd.concat([existing_products_df, add_to_completed_db_df] , ignore_index=True).fillna(-21)

        merged_df = merged_df.drop_duplicates(subset='Asin', keep="first")

        query_str3 = ','.join(map(str , merged_df.columns))
        for asin in range(len(merged_df.index)):
            merged_df.at[asin, 'Title'] = merged_df.iloc[asin].Title.replace("\\" , '').replace('"' , '')
            values = ','.join(map(value_creator , merged_df.iloc[asin].values))
            try:
                query = f'''INSERT INTO remote_completed{country} ({query_str3}) VALUES ({values})'''
                cursor.execute(query)
            except:
                try :
                    merged_df.at[asin,'Title'] = '---'
                    values = ','.join(map(value_creator , merged_df.iloc[asin].values))
                    query = f'''INSERT INTO remote_completed{country} ({query_str3}) VALUES ({values})'''
                    cursor.execute(query)
                except Exception as e:
                    print(e , values)
        ##set Is_executed to true
        query = f'''UPDATE remote_exceldata SET Is_executed = 1 , DateTime = '{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}' WHERE id = {uploaded_files_db.iloc[excel_file].id}'''
        cursor.execute(query)

        connection.commit()
    except Exception as e:
        print('HATA' , e)
cursor.close()
connection.close()
"""
cursor.execute('''UPDATE remote_completeduk SET Is_Deleted_By_User = 0 WHERE Asin = "B09YTS28PP"''')
"""