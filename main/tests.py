from requests import post , get
import json
import time

apiKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJjMWZhNzM0MC05ZTRkLTExZWQtODZkMC04OWE1ZmU0YWNlMjIiLCJzdWJJZCI6IjYzZDNkZGIwOGQ2MWZjNWQ0ODAxOGQ3ZiIsImlhdCI6MTY3NDgyOTIzMn0.xljqYsgdB3FXUc_fIA0yDnGnFs-XenMVVgYIcehtpr0'
trackingUrl = 'https://parcelsapp.com/api/v3/shipments/tracking'
shipments = [{'trackingId': 'AW018478465', 'language': 'en', 'country': 'United States'},]

# Initiate tracking request
response = post(trackingUrl, json={'apiKey': apiKey, 'shipments': shipments})

if response.status_code == 200:
    # Get UUID from response
    uuid = response.json()['uuid']
    # Function to check tracking status with UUID
    def check_tracking_status():
        response = get(trackingUrl, params={'apiKey': apiKey, 'uuid': uuid})
        if response.status_code == 200:
            if response.json()['done']:
                print('Tracking complete')
            else:
                print('Tracking in progress...')
                time.sleep(3) # sleep for N sec
                check_tracking_status()
        else:
            print(response.text)
    check_tracking_status()
else:
    print(response.text)
