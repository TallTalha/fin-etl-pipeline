# Finansal Veri ETL Boru Hattı Projesi

Bu proje, Alpha Vantage API'ından periyodik olarak hisse senedi fiyat verilerini çeken, bu verileri işleyen ve yapılandırılmış bir şekilde PostgreSQL veritabanına yükleyen modern bir ETL (Extract, Transform, Load) boru hattıdır. Proje, veri mühendisliği alanındaki en iyi pratikler (best practices) göz önünde bulundurularak modüler ve ölçeklenebilir bir yapıda geliştirilmiştir.

## ✨ Özellikler

- **Modüler Tasarım:** Sorumlulukların Ayrılması (Separation of Concerns) ilkesine uygun olarak `api`, `database`, `processing`, `config` gibi ayrı modüllere sahiptir.
- **Container Teknolojisi:** Projenin veritabanı altyapısı, `Docker` ve `Docker Compose` kullanılarak izole ve tekrar edilebilir bir ortamda çalışır.
- **Otomatik Veritabanı Kurulumu:** `init.sql` script'i sayesinde, veritabanı ve tablolar Docker container'ı ilk kez başlatıldığında otomatik olarak oluşturulur.
- **Veri Modelleme:** Veriler, analitik sorguları optimize etmek için **Yıldız Şeması** (Star Schema) mantığına uygun olarak **Boyut (Dimension)** ve **Olay (Fact)** tablolarında saklanır.
- **Güvenli Veri Yükleme:** Veritabanına veri yazma işlemleri, veri bütünlüğünü korumak için **Transaction** ve **ROLLBACK** mekanizmaları ile güvence altına alınmıştır.
- **Merkezi Konfigürasyon:** API anahtarları, veritabanı bağlantı bilgileri gibi hassas veriler ve ayarlar, `.env` ve `config` modülü aracılığıyla koddan ayrı olarak yönetilir.
- **Etkili Loglama:** Projenin her adımı, farklı seviyelerde (INFO, DEBUG, ERROR) loglanarak uygulamanın takibi ve hata ayıklaması kolaylaştırılmıştır.

## 🛠️ Teknolojiler

- **Programlama Dili:** Python 3.10+
- **Veritabanı:** PostgreSQL 15
- **Container & Orkestrasyon:** Docker, Docker Compose
- **Ana Kütüphaneler:**
  - `pandas`: Veri işleme ve dönüştürme
  - `SQLAlchemy`: Python ile veritabanı arasında ORM ve bağlantı yönetimi
  - `psycopg2-binary`: PostgreSQL için Python sürücüsü
  - `requests`: API istekleri için
  - `python-dotenv`: Ortam değişkenlerini yönetmek için

## 📂 Proje Yapısı

```
finansal_etl_projesi/
├── api/
│   └── client.py               # API'dan veri çekme mantığı
├── config/
│   ├── db_schemas.py           # Veritabanı şema (dtype) tanımları
│   └── settings.py             # Uygulama ayarları
├── database/
│   └── core.py                 # Veritabanı bağlantısı ve temel DB işlemleri
├── processing/
│   ├── loader.py               # Transaction yönetimi ve veri yükleme mantığı
│   └── transformations.py      # Gelen veriyi işleme ve DataFrame'e dönüştürme
├── postgres_setup/
│   └── init.sql                # İlk veritabanı ve tablo oluşturma script'i
├── utils/
│   └── logger.py               # Loglama yapılandırması
├── .env.example                # Örnek .env dosyası
├── .gitignore
├── docker-compose.yml          # Docker servislerinin tanımı
└── main.py                     # ETL sürecini başlatan ana script (Orkestra Şefi)
```

## 🚀 Kurulum ve Çalıştırma

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/TallTalha/fin-etl-pipeline.git](https://github.com/TallTalha/fin-etl-pipeline.git)
    cd fin-etl-pipeline
    ```

2.  **`.env` Dosyasını Oluşturun:**
    `.env.example` dosyasını kopyalayarak `.env` adında yeni bir dosya oluşturun. İçindeki `ALPHAVANTAGE_API_KEY` ve veritabanı şifresi gibi alanları kendi bilgilerinizle doldurun.

3.  **Veritabanını Başlatın:**
    Projenin ana dizininde aşağıdaki komutu çalıştırarak PostgreSQL veritabanını Docker üzerinde başlatın. Bu komut, tabloları da otomatik olarak oluşturacaktır.
    ```bash
    docker compose up -d
    ```

4.  **ETL Sürecini Çalıştırın:**
    Gerekli Python kütüphanelerini kurduktan sonra (`pip install -r requirements.txt`), ana script'i çalıştırın.
    ```bash
    python main.py
    ```
    Logları terminalden takip ederek sürecin başarıyla tamamlandığını doğrulayın.

## 🔮 Gelecek Geliştirmeler

Bu projenin mevcut temeli üzerine eklenebilecek potansiyel geliştirmeler:

- **[ ] Apache Airflow Entegrasyonu:** `main.py` script'inin manuel olarak değil, belirli zaman aralıklarıyla (örn: her saat başı) otomatik olarak çalışmasını sağlamak.
- **[ ] Boyut Tablosunu Zenginleştirme:** Farklı bir API endpoint'i kullanarak `dim_stocks` tablosuna şirket adı, sektör, piyasa değeri gibi ek bilgiler eklemek.
- **[ ] Birim Testleri (Unit Tests):** `pytest` kullanarak kritik fonksiyonların doğru çalıştığını garanti altına alan testler yazmak.
- **[ ] Parametrizasyon:** `main.py`'i, tek bir hisse yerine bir listedeki tüm hisseler için veri çekecek şekilde dinamik hale getirmek.