from django.test import TestCase


# Create your tests here.


import trackApi
from datetime import datetime 
import json

def order_track(apiKey):
    tracker = trackApi.TrackingApi(apiKey)
    tracker.sandbox = False
    tracknumber = ['T00EWA0007893145']
    post = []
    for xxx in tracknumber:
        post.append({"tracking_number": xxx, "courier_code": "hermes-uk"})
        postData = json.dumps(post)
        # create tracking number
        result = tracker.doRequest("create", postData, "POST")
        ## Get tracking results of a tracking or List all trackings
        get = f"get?tracking_numbers={xxx}"
        result = tracker.doRequest(get)
        dict = json.loads(result.decode('utf-8'))
        ## ORDER STATUS 
        data = [abc for abc in dict.get('data')][-1]
        ## CHECKPOINTS
        trackinfo = [abc for abc in data.get('origin_info').get('trackinfo')]
        ## DELIVERY STATUS 
        delivery_status = data.get('delivery_status').upper()
        ## LAST CHECKPOINT TIME
        last_cp_time = data.get('lastest_checkpoint_time')
        ##DATETIME
        date = last_cp_time.split('T')[0]
        time = last_cp_time.split('T')[1].split('+')[0]
        order_datetime = f'{date} {time}'
        order_datetime_object = datetime.strptime(order_datetime, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        passing_time = now - order_datetime_object
        if passing_time.total_seconds() <= 3600:
            lastupdate = int(passing_time.total_seconds() / 60) + "Dakika"
        elif passing_time.total_seconds() > 3600 and passing_time.total_seconds() < 86400:
            lastupdate = int(passing_time.total_seconds() /3600) + "Saat"
        elif passing_time.total_seconds() >= 86400:
            lastupdate = f"{int(passing_time.total_seconds() / 86400)} Gün"
        ##SON DURUM - KART RENGI 
        if delivery_status.lower() == "delivered":
            bg = "bg-success"
        elif int(passing_time.total_seconds() /86400)>= 2 :
            bg = "bg-warning"
        else:
            bg = "bg-primary"
        informations = {"Tracknumber" : xxx , "Status" : delivery_status , "Time" : time , "Location" :  None , "Date" : date , "lastupdate" : lastupdate , "bg" : bg}
        return informations
print(order_track(apiKey = "uh77udwn-90ld-lzge-e1ib-pmkl0ct2zl68"))