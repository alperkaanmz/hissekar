# 📈 Hissekar - Finansal Analiz Platformu

Django tabanlı modern finansal analiz ve hisse senedi takip platformu.

## 🚀 Özellikler

- **Hisse Senedi Analizi**: Gerçek zamanlı hisse verileri
- **Finansal Raporlar**: Gelir tablosu, bilanço, nakit akış analizi
- **Modern Arayüz**: Bootstrap tabanlı responsive tasarım
- **Veri Görselleştirme**: Plotly entegrasyonu
- **RESTful API**: JSON tabanlı veri erişimi

## 🛠️ Teknolojiler

- **Backend**: Django 5.0, Python 3.10
- **Frontend**: Bootstrap, Tailwind CSS
- **Database**: SQLite
- **Charts**: Plotly, Chart.js
- **Data**: yfinance, pandas

## 📦 Kurulum

1. **Repository'yi klonlayın:**
```bash
git clone <your-repo-url>
cd hissekar
```

2. **Virtual environment oluşturun:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Veritabanını hazırlayın:**
```bash
python manage.py migrate
```

5. **Şirket verilerini yükleyin:**
```bash
python manage.py load_companies
```

6. **Serveri başlatın:**
```bash
python manage.py runserver
```

7. **Tarayıcıda açın:** http://127.0.0.1:8000

## 📁 Proje Yapısı

```
hissekar/
├── core/                    # Ana Django uygulaması
│   ├── models.py           # Veri modelleri
│   ├── views.py            # View fonksiyonları
│   ├── urls.py             # URL yönlendirmeleri
│   └── management/         # Yönetim komutları
├── hissekar_project/       # Django ayarları
├── templates/              # HTML şablonları
├── static/                 # CSS, JS, resimler
├── data/                   # CSV veri dosyaları
├── requirements.txt        # Python bağımlılıkları
└── manage.py              # Django yönetim script'i
```

## 🎯 Kullanım

### Ana Sayfa
- Hisse senedi listesi ve genel durum

### Şirket Profili
- Detaylı finansal analiz
- Grafik ve tablolar
- Tarihsel veriler

### Data Tables
- Filtrelenebilir şirket listesi
- Excel/PDF export özelliği

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Proje Link: [https://github.com/yourusername/hissekar](https://github.com/yourusername/hissekar)
