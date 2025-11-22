# README.md

# Proje: Remote ve Order Track Uygulaması

Bu proje, Django ile geliştirilmiş iki temel uygulamayı içerir: **Remote App** ve **Order Track App**. Her iki uygulama da e-ticaret verilerini yönetmek ve takip etmek için tasarlanmıştır.

## İçindekiler

1. [Remote App](#remote-app)

   * [Amaç](#ama%C3%A7)
   * [Veritabanı Alanları](#veritaban%C4%B1-alanlar%C4%B1)
   * [View ve Fonksiyonlar](#view-ve-fonksiyonlar)
   * [Matematiksel Hesaplamalar](#matematiksel-hesaplamalar)
2. [Order Track App](#order-track-app)

   * [Amaç](#ama%C3%A7-1)
   * [Veritabanı Alanları](#veritaban%C4%B1-alanlar%C4%B1-1)
   * [View ve Fonksiyonlar](#view-ve-fonksiyonlar-1)
   * [Takip Mantığı](#takip-mant%C4%B1%C4%9F%C4%B1)

---

## Remote App

### Amaç

Remote App, Keepa benzeri bir ürün takip ve fiyat analiz sistemi sağlar. Kullanıcılar ürünlerini yükler ve sistem, mevcut satış verilerini, fiyatları ve Amazon verilerini işler. Bu veriler:
(EKSIK VERILER AMZSRVR REPOSUNDAKI SCRIPTLER TARAFINDAN HESAPLANIP DOLDURULUYOR)
* Ürün fiyat analizi
* Satış performansı
* Üçüncü parti satıcı fiyatları
* Stok ve Buy Box durumu

için kullanılır.

### Veritabanı Alanları

Veritabanı alanları `completed_db`, `notCompleted_db` ve `keepa_db` olarak ayrılır.

#### completed_db (Tamamlanan ürünler)

| Alan Adı           | Açıklama                                        |
| ------------------ | ----------------------------------------------- |
| User_id            | Kullanıcı ID                                    |
| Title              | Ürün başlığı                                    |
| Asin               | Amazon ASIN                                     |
| SalesRank          | Güncel satış sıralaması                         |
| SalesRank90        | 90 günlük ortalama satış sıralaması             |
| Is_Buybox_Fba      | Buy Box FBA mı?                                 |
| Fba_Seller_Count   | FBA satıcı sayısı                               |
| Amazon_Current     | Amazon fiyatı                                   |
| Buybox_Lowest      | Buy Box lowest fiyatı                           |
| Variation_Asins    | Ürün varyasyon ASIN sayısı                      |
| Weight             | Ürün ağırlığı (lbs)                             |
| Profit_Percentage  | Kar yüzdesi                                     |
| Is_Deleted_By_User | Kullanıcı tarafından silindi mi?                |
| Pool               | Pool durumu                                     |
| Date               | Veri girildiği tarih                            |
| Status             | Ürün durumu (success, warning, danger, primary) |

#### notCompleted_db (Tamamlanmamış ürünler)

| Alan Adı      | Açıklama                                 |
| ------------- | ---------------------------------------- |
| Asin          | Amazon ASIN                              |
| User_id       | Kullanıcı ID                             |
| Diğer alanlar | Yukarıdaki completed_db alanlarının çoğu |

#### keepa_db (Keepa uyumlu veriler)

| Alan Adı                | Açıklama                    |
| ----------------------- | --------------------------- |
| Asin                    | Amazon ASIN                 |
| Title                   | Ürün başlığı                |
| SalesRank               | Satış sıralaması            |
| SalesRank90             | 90 günlük ortalama sıralama |
| Drop_Count              | Son 30 gün satış düşüşü     |
| Buy_Price_FBA           | FBA alış fiyatı             |
| Buy_Price_FBM           | FBM alış fiyatı             |
| Buy_Price_BB            | Buy Box fiyatı              |
| Buy_Price_NC            | Normal alış fiyatı          |
| Sale_Price_NC           | Satış fiyatı                |
| Sale_Price_BB           | Buy Box satış fiyatı        |
| Sale_Price_FBM          | FBM satış fiyatı            |
| Sale_Price_FBA          | FBA satış fiyatı            |
| Buybox_Lowest           | Buy Box lowest              |
| Is_Buybox_Fba           | Buy Box FBA mı?             |
| Amazon_Current          | Amazon güncel fiyatı        |
| Fba_Seller_Count        | FBA satıcı sayısı           |
| Variation_Asins         | Varyasyon sayısı            |
| Weight                  | Ürün ağırlığı               |
| Referral_Fee_Percentage | Komisyon yüzdesi            |
| Pick_and_Pack_Fee       | FBA pick&pack ücreti        |

### View ve Fonksiyonlar

* **get_excels**: Kullanıcıdan gelen Excel dosyasını alır, veritabanındaki ürünlerle birleştirir ve eksik verileri doldurur.
* **check_to_notCompleted_db**: Tamamlanmamış ürünleri kontrol eder ve verileri tamamlar.
* **dataSaver**: Keepa veritabanına yeni veriler ekler.
* **get_or_create_completed**: completed_db'de olmayan ürünleri ekler.

### Matematiksel Hesaplamalar

* Ürün ağırlığı: `Weight (lbs) = max(WEIGHT * 0.0022046226, DIMENSION * 0.0610237 / 135)`
* Kar yüzdesi: `(Satış Fiyatı - Alış Fiyatı - FBA Ücretleri - Komisyon) / Satış Fiyatı * 100`
* Boş varyasyon sayısı: `Variation_Asins.count(',') + 1`

---

## Order Track App

### Amaç

Order Track App, kargo takip ve sipariş durumu izleme sistemi sağlar. Kullanıcılar Excel dosyası yükler ve sistem:

* Amazon sipariş numarasına göre kargo bilgilerini alır
* Takip numarası ve kargo firmasını veritabanına kaydeder
* Teslimat durumunu günceller
* Siparişin gecikme durumunu hesaplar

### Veritabanı Alanları

`Order` modeli alanları:

| Alan Adı      | Açıklama                           |
| ------------- | ---------------------------------- |
| AmazonOrderId | Amazon sipariş numarası            |
| Tracknumber   | Ana takip numarası                 |
| Tracknumber2  | Alternatif takip numarası          |
| Courier_Name  | Kargo firması (sistem kodu)        |
| Last_Status   | Son durum mesajı                   |
| Status        | Arka planda gösterilen durum rengi |

### View ve Fonksiyonlar

* **kargotakip (view)**:

  * Kullanıcı formu ile dosya yükler
  * order_track fonksiyonunu çağırır
  * Takip bilgilerini şablona gönderir

* **order_track (fonksiyon)**:

  * Tüm Order veritabanını okur
  * Tracking API ile güncel durumu alır
  * Son kontrol zamanına göre gecikmeyi hesaplar
  * Teslim edilen ürünleri işaretler ve renk kodu atar

* **TrackingApi**:

  * TrackingMore API ile iletişim kurar
  * POST ve GET işlemlerini yönetir

* **courier_code**:

  * Kargo firması ismini API uyumlu koda çevirir

* **uploaded_file**:

  * Excel dosyasındaki siparişleri veritabanına ekler veya günceller

### Takip Mantığı

1. Tracking numarası ve kargo firması alınır.
2. TrackingMore API ile kargo durumu sorgulanır.
3. Teslimat durumu ve son checkpoint zamanı ile geçen süre hesaplanır.
4. `lastupdate` alanı dakika, saat veya gün cinsinden hesaplanır.
5. Renk kodu atanır:

   * `success` -> Teslim edildi
   * `warning` -> 2 günden fazla gecikme
   * `danger` -> 5 günden fazla gecikme
   * `primary` -> Normal takip
6. Veriler Order modeli ile kaydedilir ve şablona gönderilir.

---


# Proje README

## Proje Genel Tanımı
Bu proje, **Amazon siparişlerini takip eden ve Keepa ile uyumlu verileri işleyen** bir Django uygulamasıdır. Proje iki ana uygulamadan oluşur:  

1. **Remote App** → Keepa’den veya benzeri kaynaklardan alınan ürün ve fiyat verilerini işler.  
2. **Order Track App** → Siparişleri takip eder, kargo durumlarını günceller ve kullanıcıya gösterir.  

Proje çoklu veritabanı kullanır:  
- `default` → Lokal veya ana veritabanı (auth, sessions, order_track vs.)  
- `mysql` → Remote app verilerini saklamak için.  

Router sınıflarıyla uygulamalar kendi veritabanına yönlendirilir:

```python
class sqLiteRouter:
    route_app_labels = {"auth", "contenttypes" , "admin" , "sessions" , "main" , "order_track" , "accounts" }
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "default"
        return None
```

```python
class mySQLRouter:
    route_app_labels = {"remote"}
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "mysql"
        return None
```

## Remote App (Keepa Verileri)

### Amaç
Remote app, Keepa’dan veya benzeri kaynaklardan çekilen **ürün fiyat ve stok bilgilerini** işler. Kullanıcıların güncel veriye göre işlem yapabilmesini sağlar.

### Temel Fonksiyon: `get_excels`
`get_excels` fonksiyonu iki excel dosyasını (completed ve target) alır ve veritabanıyla eşleştirir:

```python
def get_excels(com_file , target_file , cursor ,keepa_db_query , completed_db_query , notCompleted_db_query , user_id):
    com_pd_file = pd.read_excel(com_file)[['Title','ASIN','Buy Box: Current','New: Current','New, 3rd Party FBA: Current','New, 3rd Party FBM: Current']]
    target_pd_file = pd.read_excel(target_file)[['ASIN','Sales Rank: Current','Sales Rank: Drops last 30 days','Buy Box: Current','New: Current','New, 3rd Party FBA: Current','New, 3rd Party FBM: Current','Referral Fee %','FBA Fees:','Buy Box: Is FBA','Count of retrieved live offers: New, FBA' , 'Amazon: Current' , 'Package: Dimension (cm³)' ,  'Package: Weight (g)' , 'Sales Rank: 90 days avg.' , 'Buy Box: Lowest' , 'Variation ASINs']]
```

#### İşlevler
- Verilen Excel dosyalarını pandas ile okur ve gerekli kolonları seçer.  
- Kolon isimlerini veritabanı ile uyumlu hâle getirir (`rename`).  
- Merge işlemi ile **completed ve target verilerini birleştirir**.  
- Boş değerleri doldurur ve Keepa veritabanına ekler (`add_to_keepa_db_df`).  
- Kullanıcının veritabanında zaten bulunan ürünleri günceller veya yeni ekler.  

#### Matematiksel Mantık
- `Weight` ve `Dimension` kolonları üzerinden ürün ağırlığı ve hacimden **tahmini shipping hesaplamaları** yapılır:

```python
Weight = max(WEIGHT * 0.0022046226 , DIMENSION * 0.0610237 /135)
```

- Satış ve kâr oranları hesaplamaları, Keepa’daki fiyat verileri ile kullanıcı fiyatları arasındaki fark üzerinden yapılır.  

## Order Track App

### Amaç
Order Track app, **Amazon siparişlerini ve kargo durumlarını takip eder**. Kullanıcıya son durum ve tahmini teslim zamanı gösterilir.

### View: `kargotakip`

```python
def kargotakip(request):
    apiKey = "w7xxm92y-c73w-k4ip-l6we-yhufw5dtw51g"
    order_list = order_track(apiKey=apiKey)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file(request.FILES['file'] , Fransa)
    else:
        form = UploadFileForm()
    data = {        
            "info" : order_list , 
            'form' : form
        }
    return render(request , "kargotakip.html" , data)
```

- Kullanıcı yüklediği Excel dosyasını işler (`uploaded_file`)  
- Tüm siparişler `order_track` fonksiyonu ile güncellenir  

### Order Track Fonksiyonu: `order_track`

```python
def order_track(apiKey):
    tracker = TrackingApi(apiKey)
    tracker.sandbox = False
    order_info_list = []
    Orders = [x for x in Order.objects.values()]
    ...
    delivery_status = data.get('delivery_status').upper()
    order = Order.objects.get(Tracknumber = tracknumber)
    ...
    order.save()
```

- Tüm siparişleri alır ve Tracking API üzerinden günceller.  
- `delivery_status` alanına göre siparişin durumu (`Status`) güncellenir:  
  - `"delivered"` → success  
  - 2 gün geçti → warning  
  - 5 gün geçti → danger  

- Son checkpoint zamanı hesaplanır ve kullanıcıya `"lastupdate"` olarak gösterilir.  

### Tracking API

`TrackingApi` sınıfı, üçüncü parti kargo API’si ile haberleşir:

```python
class TrackingApi:
    baseApi = "https://api.trackingmore.com"
    apiVersion = "v3"
    def doRequest(self, api_path, post_data="", method="get"):
        ...
        req = urllib.request.Request(url, post_data, headers=headers, method=method)
        with urllib.request.urlopen(req) as response:
            return response.read()
```

- `create` isteği ile takip numarası kaydedilir  
- `get` isteği ile takip durumu alınır  

### File Upload Fonksiyonu: `uploaded_file`

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
            track = Order.objects.get(AmazonOrderId= fileAmazonOrderId[index[0]])
            if track.Tracknumber == None: track.Tracknumber = trackingID[index[0]] if trackingID[index[0]] is not None else None
            if track.Tracknumber2 == None and track.Tracknumber != trackingID[index[0]] : track.Tracknumber2 = trackingID[index[0]] if trackingID[index[0]] is not None else None
            if track.Courier_Name == None or track.Courier_Name != courier_code(carrier[index[0]]): track.Courier_Name = courier_code(carrier[index[0]]) if carrier[index[0]] is not None else None              
            track.save()            
        except Order.DoesNotExist:
            track = Order(
            AmazonOrderId  = fileAmazonOrderId[index[0]] , 
            Tracknumber = trackingID[index[0]] if trackingID[index[0]] is not None else None , 
            Courier_Name = courier_code(carrier[index[0]]) if carrier[index[0]] is not None else None 
            )
            track.save()
```

- Excel dosyası yüklenir ve Amazon siparişleri ile eşleştirilir.  
- Tracking numarası ve kargo bilgileri veritabanına kaydedilir veya güncellenir.  


