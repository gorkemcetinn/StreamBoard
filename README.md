
# 📊 Canlı Kullanıcı Dashboard : StreamBoard

Gerçek zamanlı veri akışını Kafka ve Spark ile işleyip Flask üzerinden sunan, canlı olarak kullanıcı verilerini takip edebileceğiniz bir dashboard.

---

### 🚀 Özellikler

- 🎯 **Gerçek Zamanlı Veri İşleme:** RandomUser API'den alınan veriler Kafka ile taşınır, Spark ile analiz edilir.
- 📬 **Flask REST API:** Verileri alır, saklar ve ön uca (frontend) sunar.
- 👥 **Dashboard Arayüzü:**
  - Son gelen kullanıcı bilgisi
  - Toplam kullanıcı sayısı
  - Cinsiyet dağılımı (sayaç + pasta grafik)
  - Canlı kullanıcı listesi
  - CSV dışa aktarım

---

### 🧠 Spark ve Kafka ile Veri Akışı

Bu proje **gerçek zamanlı veri işleme mimarisi** için Kafka ve Spark'ı birlikte kullanır:

#### 📦 Apache Kafka

- **Kafka**, bir mesaj kuyruğu sistemidir. Bu projede RandomUser API'den çekilen veriler Kafka'ya gönderilir.
- Üretilen veriler (`producer`), `"user-topic"` isimli bir topic üzerinden yayınlanır.

#### ⚡ Apache Spark Structured Streaming

- Spark, Kafka'dan gelen JSON verilerini anlık olarak işler.
- Spark ile `name.first` ve `name.last` alanları birleştirilerek kullanıcı adı oluşturulur.
- Sonuç verileri Flask API'ye gönderilir (`POST /add_user`).

> Bu sayede arka planda akan veriler işlenip hızlı bir şekilde web arayüzüne yansıtılır.

---

### 🛠 Gereksinimler

- Python 3.8+
- Apache Spark 3.x
- Apache Kafka
- pip paketleri:

  ```bash
  pip install flask flask-cors kafka-python requests findspark
  ```

---

### 🔧 Kurulum

1. Spark ve Kafka'yı başlatın.
2. Gerekli Python bağımlılıklarını yükleyin.
3. Aşağıdaki dosyalar hazır olmalı:
   - `main.py`
   - `app.py`
   - `randomuser_producer.py`
   - `spark_randomuser_stream.py`
   - `index.html`, `script.js`

---

### ▶️ Çalıştırma

1. Docker üzerinden Kafka ve Zookeeper'ı başlat:
```bash
cd proje-dizini
docker-compose -f docker-compose.yaml up -d
```
| docker-compose.yaml dosyası Kafka, Zookeeper ve Kafka UI (opsiyonel) içermelidir.

2. Ana uygulamayı başlat:

```bash
python main.py
```

> Flask + Kafka Producer + Spark Streaming birlikte başlatılır.

---

### 📁 API Uç Noktaları

| Yöntem | URL               | Açıklama                 |
|--------|-------------------|--------------------------|
| GET    | `/users`          | Tüm kullanıcıları getirir |
| GET    | `/last_user`      | Son kullanıcıyı getirir   |
| GET    | `/stats`          | Erkek/Kadın sayısını getirir |
| GET    | `/export/csv`     | CSV olarak dışa aktarır  |
| POST   | `/add_user`       | Kullanıcı ekler (Spark tarafından kullanılır) |

---

### 📸 Dashboard Özeti

- Son kullanıcı kutusu
- Toplam kullanıcı sayısı
- Cinsiyet dağılımı (sayaç + pasta grafik)
- Otomatik güncellenen kullanıcı listesi
- CSV indir butonu

---

### 📂 Örnek Ekran Görüntüsü



https://github.com/user-attachments/assets/03ab6ccf-662e-47bb-a8c5-65878dfcf8a6


🧩 Notlar

Kafka UI arayüzüne http://localhost:8080 adresinden erişebilirsin.

Spark, streaming query'leri terminalde gösterebilir.
