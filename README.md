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

Bu README, projenin hem Remote hem de Order Track uygulamalarının tüm alanlarını, matematiksel mantığını ve işlevlerini kapsamlı olarak içerir.
