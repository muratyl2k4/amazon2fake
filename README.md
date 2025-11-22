Tamam, işte projen için **tek bir README.md** dosyası, tüm app’ler, tablolar, field’lar, view’lar, Excel kolonları, API akışı ve matematiksel işlemler dahil olacak şekilde hazırlanmış hâli:

````markdown
# Proje Dokümantasyonu

Bu doküman, projenin **Remote** ve **Order_Track** app’lerini, veritabanı tablolarını, view’ları, Excel mapping’lerini, API akışlarını ve hesaplamaları kapsayan kapsamlı bir özetidir.

---

## İçindekiler
1. [Remote App](#remote-app)
   - Modeller ve Alanlar
   - Excel İşleme (get_excels)
   - Keepa ve Completed DB İşlemleri
   - Matematiksel Hesaplamalar
2. [Order_Track App](#order_track-app)
   - Modeller ve Alanlar
   - Views (kargotakip)
   - Tracking API
   - File Upload İşlemleri
   - Courier Mapping
3. [Veritabanı Router’ları](#veritabanı-routerları)
4. [Excel Kolonları ve Mapping](#excel-kolonları-ve-mapping)
5. [Matematiksel Hesaplamalar ve Zaman İşlemleri](#matematiksel-hesaplamalar-ve-zaman-işlemleri)

---

## Remote App

### Modeller ve Alanlar

**Keepa DB:**
| Field | Tip | Açıklama |
|-------|-----|----------|
| Asin | String | Ürün ASIN kodu |
| Title | String | Ürün başlığı |
| SalesRank | Integer | Anlık satış sıralaması |
| SalesRank90 | Integer | 90 günlük ortalama satış sıralaması |
| Drop_Count | Integer | Son 30 gündeki düşüş sayısı |
| Buy_Price_FBA | Float | FBA fiyatı |
| Buy_Price_FBM | Float | FBM fiyatı |
| Buy_Price_BB | Float | Buy Box fiyatı |
| Buy_Price_NC | Float | Normal fiyat |
| Sale_Price_FBA | Float | FBA satış fiyatı |
| Sale_Price_FBM | Float | FBM satış fiyatı |
| Sale_Price_BB | Float | Buy Box satış fiyatı |
| Sale_Price_NC | Float | Normal satış fiyatı |
| Referral_Fee_Percentage | Float | Komisyon yüzdesi |
| Pick_and_Pack_Fee | Float | FBA işlemi ücreti |
| Is_Buybox_Fba | Boolean | BuyBox FBA mı? |
| Fba_Seller_Count | Integer | FBA satıcı sayısı |
| Amazon_Current | Float | Amazon fiyatı |
| Dimension | Float | Paket hacmi (cm³) |
| Weight | Float | Paket ağırlığı (g) |
| Buybox_Lowest | Float | En düşük BuyBox fiyatı |
| Variation_Asins | Integer | Varyasyon sayısı |

**Completed DB:**
| Field | Tip | Açıklama |
|-------|-----|----------|
| User_id | Integer | Kullanıcı ID |
| Title | String | Ürün başlığı |
| Asin | String | Ürün ASIN kodu |
| SalesRank | Integer | Anlık satış sıralaması |
| SalesRank90 | Integer | 90 günlük ortalama satış sıralaması |
| Is_Buybox_Fba | Boolean | BuyBox FBA mı? |
| Fba_Seller_Count | Integer | FBA satıcı sayısı |
| Amazon_Current | Float | Amazon fiyatı |
| Buybox_Lowest | Float | En düşük BuyBox fiyatı |
| Variation_Asins | Integer | Varyasyon sayısı |
| Weight | Float | Ağırlık |
| Profit_Percentage | Float | Kar yüzdesi |
| Date | DateTime | Kaydedilme tarihi |
| Is_Deleted_By_User | Boolean | Kullanıcı tarafından silinmiş mi |
| Pool | Boolean | Havuzda mı? |

### Excel İşleme

Fonksiyon: `get_excels(com_file, target_file, cursor, keepa_db_query, completed_db_query, notCompleted_db_query, user_id)`

- **Amaç:** Com ve Target Excel dosyalarını okuyup, veritabanı tabloları ile eşleştirir.
- **Adımlar:**
  1. Excel dosyaları pandas ile okunur.
  2. Kolonlar normalize edilir (`rename`).
  3. Merge işlemi yapılır.
  4. DB kayıtlarıyla karşılaştırılır, eksik veya değişmiş veriler güncellenir.
  5. Keepa DB için yeni kayıtlar hazırlanır.
- **Çıktılar:**
  - `change_IDBU_true_df`
  - `existing_products_df`
  - `Asins_to_delete_from_notCompleted`
  - `fill_empty_rows_df`
  - `add_to_keepa_db_df`
  - `new_completed_db_df`

---

## Order_Track App

### Modeller ve Alanlar

**Order Model:**
| Field | Tip | Açıklama |
|-------|-----|----------|
| AmazonOrderId | String | Amazon sipariş numarası |
| Tracknumber | String | Birincil kargo takip numarası |
| Tracknumber2 | String | İkincil kargo takip numarası |
| Courier_Name | String | Kargo şirketi kodu |
| Last_Status | String | Son durum |
| Status | String | Bootstrap renk kodu (primary, warning, success, danger) |

### Views

**kargotakip view:**
```python
def kargotakip(request):
    apiKey = "YOUR_API_KEY"
    order_list = order_track(apiKey=apiKey)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file(request.FILES['file'] , Fransa)
    else:
        form = UploadFileForm()
    data = {"info": order_list, "form": form}
    return render(request, "kargotakip.html", data)
````

* Kullanıcı Excel yükleyebilir.
* API üzerinden kargo durumları çekilir.
* View template’e gönderilir.

### Tracking API

`trackApi.py`:

```python
import urllib
class TrackingApi:
    baseApi = "https://api.trackingmore.com"
    apiVersion = "v3"
    sandbox = False

    def __init__(self, api_key):
        self.apiKey = api_key

    def doRequest(self, api_path, post_data="", method="get"):
        method = method.upper()
        url = f"{self.baseApi}/{self.apiVersion}/trackings/{api_path}"
        if self.sandbox:
            url = f"{self.baseApi}/{self.apiVersion}/trackings/sandbox/{api_path}"
        headers = {"Content-Type": "application/json", "Tracking-Api-Key": self.apiKey,
                   'User-Agent': 'Mozilla/5.0'}
        post_data = post_data.encode('UTF-8')
        req = urllib.request.Request(url, post_data, headers=headers, method=method)
        with urllib.request.urlopen(req) as response:
            return response.read()
```

### File Upload İşlemleri

`fileupload.py`:

```python
def uploaded_file(file , data):
    pd_file = pd.read_excel(file)
    pd_file = pd_file.where(pd.notnull(pd_file), None)
    carrier = [x for x in pd_file['Carrier']]
    trackingID = [x for x in pd_file['Tracking ID']]
    fileAmazonOrderId = [x for x in pd_file['AmazonOrderId']]
    dbAmazonOrderId = [x.get('SATICI_SIPARIS_NUMARASI') for x in data.objects.values()]
    common_tracks = common_member(fileAmazonOrderId , dbAmazonOrderId)
    for i in common_tracks:
        index = pd_file.index[pd_file['AmazonOrderId'] == i].tolist()
        try:
            track = Order.objects.get(AmazonOrderId=fileAmazonOrderId[index[0]])
            if track.Tracknumber == None: track.Tracknumber = trackingID[index[0]]
            if track.Tracknumber2 == None and track.Tracknumber != trackingID[index[0]]: track.Tracknumber2 = trackingID[index[0]]
            if track.Courier_Name == None or track.Courier_Name != courier_code(carrier[index[0]]): track.Courier_Name = courier_code(carrier[index[0]])
            track.save()
        except Order.DoesNotExist:
            track = Order(AmazonOrderId=fileAmazonOrderId[index[0]], Tracknumber=trackingID[index[0]],
                          Courier_Name=courier_code(carrier[index[0]]))
            track.save()
```

### Courier Mapping

`courier_code.py`:

```python
import pandas
def courier_code(companyName):
    csv = pandas.read_csv("order_track/c.csv")
    courier_name = companyName.lower().replace('ı','i')
    if courier_name == 'dpd': courier_name = 'wndirect'
    csv["Courier Name\t"] = csv["Courier Name\t"].str.lower()
    result = csv[csv["Courier Name\t"] == courier_name+ '\t'] if not csv[csv["Courier Name\t"] == courier_name+ '\t'].empty else csv[csv["Courier Name\t"].str.contains(courier_name.lower())]
    return result['Carrier Code\t'].values[0].replace('\t','')
```

---

## Veritabanı Router’ları

**sqLiteRouter**

* `auth`, `contenttypes`, `admin`, `sessions`, `main`, `order_track`, `accounts` için `default` DB kullanır.

**mySQLRouter**

* `remote` app için `mysql` DB kullanır.

---

## Excel Kolonları ve Mapping

| Com File                                 | Target File                 | DB Column               |
| ---------------------------------------- | --------------------------- | ----------------------- |
| Title                                    | Title                       | Title                   |
| ASIN                                     | ASIN                        | Asin                    |
| Buy Box: Current                         | Buy Box: Current            | Buy_Price_BB            |
| New: Current                             | New: Current                | Buy_Price_NC            |
| New, 3rd Party FBA: Current              | New, 3rd Party FBA: Current | Buy_Price_FBA           |
| New, 3rd Party FBM: Current              | New, 3rd Party FBM: Current | Buy_Price_FBM           |
| Sales Rank: Current                      | SalesRank                   | SalesRank               |
| Sales Rank: Drops last 30 days           | Drop_Count                  | Drop_Count              |
| Referral Fee %                           | Referral_Fee_Percentage     | Referral_Fee_Percentage |
| FBA Fees:                                | Pick_and_Pack_Fee           | Pick_and_Pack_Fee       |
| Buy Box: Is FBA                          | Is_Buybox_Fba               | Is_Buybox_Fba           |
| Count of retrieved live offers: New, FBA | Fba_Seller_Count            | Fba_Seller_Count        |
| Amazon: Current                          | Amazon_Current              | Amazon_Current          |
| Package: Dimension (cm³)                 | Dimension                   | Dimension               |
| Package: Weight (g)                      | Weight                      | Weight                  |
| Sales Rank: 90 days avg.                 | SalesRank90                 | SalesRank90             |
| Buy Box: Lowest                          | Buybox_Lowest               | Buybox_Lowest           |
| Variation ASINs                          | Variation_Asins             | Variation_Asins         |

---

## Matematiksel Hesaplamalar ve Zaman İşlemleri

* **Weight & Dimension:**

```python
Weight = max(WEIGHT * 0.0022046226 , DIMENSION * 0.0610237 /135)
```

* **Geçen süre hesaplama:**

```python
passing_time = now - order_datetime_object
if passing_time.total_seconds() <= 3600: lastupdate = f"{passing_time.total_seconds()/60} Dakika"
elif passing_time.total_seconds() <= 86400: lastupdate = f"{passing_time.total_seconds()/3600} Saat"
else: lastupdate = f"{passing_time.total_seconds()/86400} Gün"
```

* **Sipariş durumu renkleri:**

  * Delivered → success
  * 2+ gün → warning
  * 5+ gün → danger
  * Diğer → primary




Bunu yapmamı ister misin?
```
