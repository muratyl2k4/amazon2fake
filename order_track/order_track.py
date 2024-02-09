from .models import Order
from .trackApi import TrackingApi
from datetime import datetime 
import json
def order_track(apiKey):
    ###TODO 15 gun
    tracker = TrackingApi(apiKey)
    tracker.sandbox = False
    order_info_list = []
    Orders = [x for x in Order.objects.values()]
    post = []
    for ord in Orders:
        try : 
            tracknumber = ord.get('Tracknumber') if ord.get('Tracknumber2') == None else ord.get('Tracknumber2')
            courier_code = ord.get('Courier_Name')
            post.append({"tracking_number": tracknumber , "courier_code": courier_code})
            postData = json.dumps(post)
            # create tracking number
            result = tracker.doRequest("create", postData, "POST")
            ## Get tracking results of a tracking or List all trackings
            get = f"get?tracking_numbers={tracknumber}"
            result = tracker.doRequest(get)
            dict = json.loads(result.decode('utf-8'))
            ## ORDER STATUS 
            data = [abc for abc in dict.get('data')][-1]
            print(data)
            ## DELIVERY STATUS 
            delivery_status = data.get('delivery_status').upper()
            order = Order.objects.get(Tracknumber = tracknumber)
            if order.Last_Status == None or order.Last_Status != 'DELIVERED' : order.Last_Status = 'Tracking in Progress...'
            ## LAST CHECKPOINT TIME
            last_cp_time = data.get('lastest_checkpoint_time')
            ##DATETIME
            date = last_cp_time.split('T')[0]
            time = last_cp_time.split('T')[1].split('+')[0]
            order_datetime = f'{date} {time}'
            order_datetime_object = datetime.strptime(order_datetime, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            passing_time = now - order_datetime_object
            ## GECENSURE
            if passing_time.total_seconds() <= 3600: lastupdate = int(passing_time.total_seconds() / 60) + "Dakika"
            elif passing_time.total_seconds() > 3600 and passing_time.total_seconds() < 86400: lastupdate = int(passing_time.total_seconds() /3600) + "Saat"
            elif passing_time.total_seconds() >= 86400: lastupdate = f"{int(passing_time.total_seconds() / 86400)} Gün"
            ##SON DURUM - KART RENGI 
            if delivery_status.lower() == "delivered": status = "success"
            elif int(passing_time.total_seconds() /86400)>= 2 : status = "warning"
            elif int(passing_time.total_seconds() /86400)>= 5 : status = "danger"
            else: status = "primary"
            order.Status = status
            order.save()
            ##LINK 
            if courier_code == 'hermes-uk' : weblink = f'https://www.evri.com/track/parcel/{tracknumber}/details'
            else : weblink = f'https://parcelsapp.com/en/tracking/{tracknumber}'
            informations = {"OrderID" : order.AmazonOrderId, "Tracknumber" : tracknumber , "Status" : delivery_status , "Time" : time , "Location" :  None , "Date" : date , "lastupdate" : lastupdate , 'bg' : status ,  'weblink' : weblink}
            order_info_list.append(informations)
        except Exception as e: 
            print('KARGO TAKIP HATASI : ', ord , e)
            
    return order_info_list   
    