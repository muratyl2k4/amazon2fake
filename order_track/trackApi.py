import urllib
class TrackingApi:
        
        apiPath = ""
        baseApi = "https://api.trackingmore.com"
        apiVersion = "v3"
        sandbox = False

        def __init__(self, api_key):
            self.apiKey = api_key

        def doRequest(self, api_path, post_data="", method="get"):
            method = method.upper()
            if self.sandbox:
                url = self.baseApi + "/" + self.apiVersion + "/trackings/sandbox/" + api_path
            else:
                url = self.baseApi + "/" + self.apiVersion + "/trackings/" + api_path
            headers = {"Content-Type": "application/json", "Tracking-Api-Key": self.apiKey,
                    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) '
                                    'Chrome/24.0.1312.27 Safari/537.17'}
            post_data = post_data.encode('UTF-8')
            req = urllib.request.Request(url, post_data, headers=headers, method=method)
            with urllib.request.urlopen(req) as response:
                return response.read()